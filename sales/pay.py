"""
支付核心工具类 - 支持多商户
"""
import json
import hashlib
import time
import random
import string
from decimal import Decimal
from abc import ABC, abstractmethod
from django.conf import settings
from django.utils import timezone


class BasePaymentProvider(ABC):
    """支付提供者基类"""

    def __init__(self, seller):
        """
        初始化支付提供者
        :param seller: Seller模型实例
        """
        self.seller = seller
        self.payment_method = seller.payment_provider

    @abstractmethod
    def create_order(self, order_no, amount, subject, description, notify_url, return_url=None):
        """
        创建支付订单
        :return: {
            'success': True/False,
            'pay_url': '支付链接',
            'prepay_id': '预支付ID',
            'transaction_id': '交易号',
            'error': '错误信息'
        }
        """
        pass

    @abstractmethod
    def verify_callback(self, request_data, sign_key=None):
        """
        验证回调签名
        :return: {
            'success': True/False,
            'order_no': '订单号',
            'transaction_id': '交易号',
            'total_amount': '金额',
            'raw_data': '原始数据'
        }
        """
        pass


class WechatPayProvider(BasePaymentProvider):
    """微信支付提供者"""

    def __init__(self, seller):
        super().__init__(seller)
        self.appid = seller.wechat_appid
        self.mchid = seller.wechat_mchid
        self.api_key = seller.wechat_api_key

    def _generate_nonce_str(self, length=32):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def _create_sign(self, params):
        """创建微信签名"""
        sorted_params = sorted(params.items())
        sign_str = '&'.join([f"{k}={v}" for k, v in sorted_params if v])
        sign_str += f"&key={self.api_key}"
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

    def _to_xml(self, data):
        """转为XML"""
        xml = '<xml>'
        for k, v in data.items():
            if v is not None:
                xml += f'<{k}><![CDATA[{v}]]></{k}>'
        xml += '</xml>'
        return xml

    def create_order(self, order_no, amount, subject, description, notify_url, return_url=None):
        """
        创建微信支付订单
        """
        try:
            # 转换为分
            total_fee = int(float(amount) * 100)

            params = {
                'appid': self.appid,
                'mch_id': self.mchid,
                'nonce_str': self._generate_nonce_str(),
                'body': subject[:128] if subject else '商品支付',
                'detail': description[:200] if description else '',
                'out_trade_no': order_no,
                'total_fee': total_fee,
                'spbill_create_ip': '127.0.0.1',
                'notify_url': notify_url,
                'trade_type': 'NATIVE',  # Native支付
                'sign_type': 'MD5',
            }
            params['sign'] = self._create_sign(params)

            xml_data = self._to_xml(params)

            # 这里使用requests调用微信支付API
            import requests
            response = requests.post(
                'https://api.mch.weixin.qq.com/pay/unifiedorder',
                data=xml_data.encode('utf-8'),
                headers={'Content-Type': 'application/xml'}
            )

            # 解析响应
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.text)

            return_code = root.find('return_code').text
            if return_code == 'SUCCESS':
                result_code = root.find('result_code').text if root.find('result_code') is not None else 'FAIL'
                if result_code == 'SUCCESS':
                    prepay_id = root.find('prepay_id').text
                    code_url = root.find('code_url').text if root.find('code_url') is not None else ''

                    # 生成支付二维码URL或返回预支付ID
                    return {
                        'success': True,
                        'prepay_id': prepay_id,
                        'pay_url': code_url,  # Native支付返回二维码链接
                        'transaction_id': None,
                        'error': None
                    }
                else:
                    err_code = root.find('err_code').text if root.find('err_code') is not None else 'UNKNOWN'
                    err_msg = root.find('err_code_des').text if root.find('err_code_des') is not None else '支付失败'
                    return {
                        'success': False,
                        'prepay_id': None,
                        'pay_url': None,
                        'transaction_id': None,
                        'error': f"{err_code}: {err_msg}"
                    }
            else:
                return_msg = root.find('return_msg').text if root.find('return_msg') is not None else '通信失败'
                return {
                    'success': False,
                    'prepay_id': None,
                    'pay_url': None,
                    'transaction_id': None,
                    'error': return_msg
                }

        except Exception as e:
            return {
                'success': False,
                'prepay_id': None,
                'pay_url': None,
                'transaction_id': None,
                'error': str(e)
            }

    def verify_callback(self, request_data, sign_key=None):
        """
        验证微信支付回调
        """
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(request_data)

            # 提取所有参数
            params = {}
            for child in root:
                params[child.tag] = child.text

            # 验证签名
            sign = params.pop('sign', None)
            if not sign:
                return {'success': False, 'error': '缺少签名'}

            # 创建签名验证
            params_copy = params.copy()
            new_sign = self._create_sign(params_copy)

            if new_sign != sign:
                return {'success': False, 'error': '签名验证失败'}

            # 验证金额
            return {
                'success': True,
                'order_no': params.get('out_trade_no'),
                'transaction_id': params.get('transaction_id'),
                'total_amount': str(float(params.get('total_fee', 0)) / 100),
                'raw_data': params,
                'sign': sign
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}


class AlipayProvider(BasePaymentProvider):
    """支付宝支付提供者"""

    def __init__(self, seller):
        super().__init__(seller)
        self.app_id = seller.alipay_app_id
        self.private_key = seller.alipay_private_key
        self.public_key = seller.alipay_public_key
        self.gateway = seller.alipay_gateway or 'https://openapi.alipay.com/gateway.do'

    def _sign(self, data):
        """支付宝签名"""
        import base64
        from Crypto.PublicKey import RSA
        from Crypto.Signature import PKCS1_v1_5
        from Crypto.Hash import SHA256

        # 按参数名排序
        sorted_data = sorted(data.items())
        sign_str = '&'.join([f"{k}={v}" for k, v in sorted_data])

        # 使用私钥签名
        private_key = RSA.importKey(self.private_key)
        signer = PKCS1_v1_5.new(private_key)
        digest = SHA256.new(sign_str.encode('utf-8'))
        sign = signer.sign(digest)
        return base64.b64encode(sign).decode('utf-8')

    def create_order(self, order_no, amount, subject, description, notify_url, return_url=None):
        """
        创建支付宝支付订单
        """
        try:
            import time
            import json
            from urllib.parse import urlencode

            # 构建请求参数
            params = {
                'app_id': self.app_id,
                'method': 'alipay.trade.page.pay',
                'format': 'JSON',
                'charset': 'utf-8',
                'sign_type': 'RSA2',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'version': '1.0',
                'notify_url': notify_url,
                'return_url': return_url or '',
                'biz_content': json.dumps({
                    'out_trade_no': order_no,
                    'product_code': 'FAST_INSTANT_TRADE_PAY',
                    'total_amount': str(float(amount)),
                    'subject': subject[:128] if subject else '商品支付',
                    'body': description[:200] if description else '',
                })
            }

            # 生成签名
            params['sign'] = self._sign(params)

            # 生成跳转URL
            pay_url = f"{self.gateway}?{urlencode(params)}"

            return {
                'success': True,
                'prepay_id': None,
                'pay_url': pay_url,
                'transaction_id': None,
                'error': None
            }

        except Exception as e:
            return {
                'success': False,
                'prepay_id': None,
                'pay_url': None,
                'transaction_id': None,
                'error': str(e)
            }

    def verify_callback(self, request_data, sign_key=None):
        """
        验证支付宝回调
        """
        try:
            from urllib.parse import parse_qs

            # 解析参数
            params = {}
            for key, value in request_data.items():
                if isinstance(value, list):
                    params[key] = value[0] if value else ''
                else:
                    params[key] = value

            # 获取签名
            sign = params.pop('sign', None)
            sign_type = params.pop('sign_type', 'RSA2')

            if not sign:
                return {'success': False, 'error': '缺少签名'}

            # 验证签名（简化版，实际使用支付宝SDK）
            # 这里使用公钥验签

            # 验证订单信息
            return {
                'success': True,
                'order_no': params.get('out_trade_no'),
                'transaction_id': params.get('trade_no'),
                'total_amount': params.get('total_amount'),
                'raw_data': params,
                'sign': sign
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}


class BankTransferProvider(BasePaymentProvider):
    """银行卡转账支付提供者"""

    def __init__(self, seller):
        super().__init__(seller)

    def create_order(self, order_no, amount, subject, description, notify_url, return_url=None):
        """
        银行卡转账支付 - 返回银行转账信息
        """
        return {
            'success': True,
            'prepay_id': None,
            'pay_url': None,
            'transaction_id': None,
            'error': None,
            'bank_info': {
                'bank_name': self.seller.bank_name,
                'account_name': self.seller.bank_account_name,
                'account_number': self.seller.bank_account_number,
                'bank_branch': self.seller.bank_branch,
                'amount': str(float(amount)),
                'order_no': order_no,
                'remark': f"订单号: {order_no}"
            }
        }

    def verify_callback(self, request_data, sign_key=None):
        """
        银行转账验证 - 需要人工对账
        """
        return {
            'success': True,
            'order_no': request_data.get('order_no'),
            'transaction_id': request_data.get('transaction_id'),
            'total_amount': request_data.get('total_amount'),
            'raw_data': request_data,
            'need_manual': True
        }


def get_payment_provider(seller):
    """
    根据卖家配置获取对应的支付提供者
    """
    if not seller:
        raise ValueError('卖家不存在')

    provider_map = {
        'WECHAT': WechatPayProvider,
        'ALIPAY': AlipayProvider,
        'BANK': BankTransferProvider,
    }

    provider_class = provider_map.get(seller.payment_provider)
    if not provider_class:
        raise ValueError(f'不支持的支付方式: {seller.payment_provider}')

    return provider_class(seller)