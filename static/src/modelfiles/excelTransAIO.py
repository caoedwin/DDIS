# -*- coding:utf-8 -*-
import pandas as pd
import pprint
from pathlib import Path
import os, sys
import warnings

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
from PyQt5 import QtCore, QtGui, QtWidgets
from Excel_InputAIO import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QThread
from Progress import UI_Progress,MyWindow
from Progressyuanhuan2 import Progress
from PyQt5.QtGui import *
from io import StringIO

class CheckFun(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super(CheckFun, self).__init__()
        self.setupUi(self)
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.myth1 = mythread1()

        self.pushButton.clicked.connect(self.start_excel)
        # self.button_clicked_signal.connect(self.excel)
        self.myth1.infobox_signal.connect(self.boxinfo)
        self.myth1.disable_button_signal.connect(self.disable_button)
        self.myth1.enable_button_signal.connect(self.enable_button)
        self.myth1.Progress_signal.connect(self.enableProgress)

    def start_excel(self):
        #方式1：全局变量global-保存到磁盘
        global Customer, Phase
        Customer = ''
        Phase = ''
        if self.radioButton.isChecked():
            Customer = self.radioButton.text()
        elif self.radioButton_5.isChecked():
            Customer = self.radioButton_5.text()
        if self.radioButton_2.isChecked():
            Phase = self.radioButton_2.text()
        elif self.radioButton_3.isChecked():
            Phase = self.radioButton_3.text()
        elif self.radioButton_4.isChecked():
            Phase = self.radioButton_4.text()
        # #方式2：对象StringIO-保存到内存,S = StringIO()定义在类外面
        # S = StringIO()
        # S.write()
        # S.getvalue()
        print(Customer,Phase)
        self.myth1.start()#pyqt5调用多线程的固定方法，调用子线程的run方法

    def disable_button(self):
        print("disable")
        self.pushButton.setEnabled(False)
        # self.textEdit_7.setMarkdown("正在运行")
        self.label_5.setText("正在运行")

    def enable_button(self):
        print("enable_button")
        self.pushButton.setEnabled(True)
        # self.textEdit_7.setMarkdown("运行完成")
        self.label_5.setText("运行完成")
        self.label_5.setStyleSheet("font: 9pt \"楷体\";\n"
                                   "color: rgb(0, 255, 0);\n"
                                   "font-weight:bold;")

    def boxinfo(self,str):
        print(str)
        if '已完成' in str:
            self.r.close()
        QtWidgets.QMessageBox.information(self, 'What?', '%s' % str)
        if '已完成' in str:
            self.close()

    def enableProgress(self):
        print("enableProgress")
        # self.child = MyWindow()
        # self.child.set_loader()
        # self.child.show()
        # app = QApplication(sys.argv)
        if Phase == "EELP+":
            self.r = Progress("<a link='b'>运行中...</a>", 45)
        elif Phase == "B(SDV)" or Phase == "C(SIT)":
            self.r = Progress("<a link='b'>运行中...</a>", 60)
        self.r.show()
        # sys.exit(app.exec_())


class mythread1(QThread):
    My_excel_result = pyqtSignal(str)
    disable_button_signal = pyqtSignal()
    enable_button_signal = pyqtSignal()
    infobox_signal = pyqtSignal(str)
    Progress_signal = pyqtSignal()
    def __init__(self):

        super(mythread1, self).__init__()
        self.excel_result = ''

    def run(self): #QThreat 被主程式用start调用时，就是首先运行run方法
        print('run')
        self.gettext()
        self.My_excel_result.emit(self.excel_result)#运行结束，发送带参信号

    def gettext(self):
        self.Customer = Customer
        self.Phase = Phase
        if self.Customer == '' or self.Phase == '':
            # print('what')
            self.infobox_signal.emit('貌似有没有选的啊，快去选一个吧！')
        else:
            self.excel()
    def excel(self):
        import os, sys

        # path1 = os.path.dirname(__file__)  # 当前文件所在的目录
        # os.path.abspath('.')
        path1 = os.path.dirname(os.path.realpath(sys.executable))
        # path2 = os.path.dirname(os.path.dirname(os.path.realpath(sys.executable)))
        Customer = "C38(NB)"
        sheetnum = self.Phase
        self.src_file = path1 + "\ProjectAIO.xlsx"
        if not os.path.exists(self.src_file):
            self.infobox_signal.emit('同级目录下没有ProjectAIO.xlsx')
        else:
            self.do_process()

    def do_process(self):
        print("do_process")
        self.disable_button_signal.emit()
        self.Progress_signal.emit()
        self.doexcel()


    def doexcel(self):
        print('doexcel')

        src_file = self.src_file
        # print(src_file)
        # 每次都需要修改的路径
        # with open('src_file.txt', 'w') as f:  # 设置文件对象
        #     print(src_file, file=f)
        # sheet_name默认为0，即读取第一个sheet的数据
        # df = pd.read_excel(src_file, header=1, sheet_name='SW Test planning')
        Customer = self.Customer
        sheetnum = self.Phase
        if sheetnum == "EELP+":
            sheetnum = '4'
        elif sheetnum == "C(SIT)":
            sheetnum = '3'
        elif sheetnum == "B(SDV)":
            sheetnum = '2'
        if sheetnum == '2':
            df = pd.read_excel(src_file, header=5, sheet_name=int(sheetnum)).iloc[:,
                 2:]  # ‘,’前面是行，后面是列，sheet_name指定sheet，可是是int第几个，可以是名称，header从第几行开始读取
            # print(df.shape)#获取行数列数
            # if 'Unnamed: 26' in df.columns:
            #     # print(1)
            #     df = df.drop(labels='Unnamed: 26', axis=1)
            print(df.shape)  # 获取行数列数
            # # 显示所有列
            pd.set_option('display.max_columns', None)
            # # 显示所有行
            # pd.set_options('display.max_rows', None)
            # print(df.columns)
            # print(df.iloc[:1, :])
            # pprint.pprint(df)
            # sheet = pd.read_excel(src_file, sheet_name=0)
            # print(sheet)
            # print(df)
            # 转换字典
            # df_dict = df.to_dict(orient='records')
            # 转换列表
            # df_list = df.values
            # # pprint.pprint(df_list)
            # print(df_list[0])
            # 注意带上inplace=True参数用于更新作用于本数据集，而不是返回一个新的数据集。
            # df.rename(columns={'6-英语':'english'},inplace=True)
            # 如果需要重命名行索引，可以通过df.rename(index={‘原索引’:‘重命名索引’})的方式进行重命名。
            # 更多的，如果要重命名多个列，可以传入一个需要重命名的多个字典值，进行多个列的重命名。
            # df[['1-学号','2-姓名','3-年龄']].rename(columns={'1-学号':'ID','2-姓名':'name','3-年龄':'age'})
            columnsRename = {
                'Category': 'Category', 'Test Title': 'TestTitle', 'Sub test title': 'Subtesttitle',
                'Test Item': 'TestItem', 'Priority': 'Priority', 'Release Date': 'ReleaseDate', 'Owner ': 'Owner',
                # 'Version': 'Version',
                'Actual Time': 'AT_Totaltime',
                'Unnamed: 10': 'AT_AttendTime', 'Unnamed: 11': 'AT_UnattendTime', 'Unnamed: 12': 'AT_Automation',
                'DQMS Test Plan': 'DQMS_AttendTime', 'Unnamed: 14': 'DQMS_UnattendTime',
                'Test Units\n/Config': 'TestUnitsConfig', 'Smart Item': 'SmartItem',
                'AIO SW Test plan Matrix for Planning': 'Cusumer', 'Unnamed: 18': 'Commercial', 'Unnamed: 19': 'SDV',
                'Unnamed: 20': 'SIT', 'Unnamed: 21': 'Coverage',
                'Feature Support': 'FeatureSupport', 'Base time-support': 'Basetimesupport', 'TE': 'TE',
                'Schedule': 'Schedule',
                'Config-all test units': 'Configalltestunits', 'Config-all test time': 'Configalltesttime',
                'Config-Automation Item': 'ConfigAutomationItem', 'Config-Automation time': 'ConfigAutomationtime',
                'Config-Leverage Item': 'ConfigLeverageItem',
                'Config-Leverage time': 'ConfigLeveragetime', 'Config-Smart Item占总case比例': 'ConfigSmartItemper',
                'Config-Smart time': 'ConfigSmarttime',
                'Comments': 'Comments', 'Project test SKU-Optimize': 'ProjecttestSKUOptimize',
                'Attend time-Optimize': 'AttendtimeOptimize',
                'Planning after Optimize': 'SKU1', 'Unnamed: 38': 'SKU2', 'Unnamed: 39': 'SKU3', 'Unnamed: 40': 'SKU4',
                'Unnamed: 41': 'SKU5',
                'Unnamed: 42': 'SKU6', 'Unnamed: 43': 'SKU7', 'Unnamed: 44': 'SKU8', 'Unnamed: 45': 'SKU9',
                'Unnamed: 46': 'SKU10', 'Config-Retest Cycle': 'ConfigRetestCycle',
                'Config-Retest SKU': 'ConfigRetestSKU', 'Config-Retest time': 'ConfigRetesttime',
            }
            if 'Unnamed: 47' in df.columns:
                columnsRename["Unnamed: 47"] = "SKU11"
            if 'Unnamed: 48' in df.columns:
                columnsRename["Unnamed: 48"] = "SKU12"
            if 'Unnamed: 49' in df.columns:
                columnsRename["Unnamed: 49"] = "SKU13"
            if 'Unnamed: 50' in df.columns:
                columnsRename["Unnamed: 50"] = "SKU14"
            if 'Unnamed: 51' in df.columns:
                columnsRename["Unnamed: 51"] = "SKU15"
            if 'Unnamed: 52' in df.columns:
                columnsRename["Unnamed: 52"] = "SKU16"
            if 'Unnamed: 53' in df.columns:
                columnsRename["Unnamed: 53"] = "SKU17"
            if 'Unnamed: 54' in df.columns:
                columnsRename["Unnamed: 54"] = "SKU18"
            if 'Unnamed: 55' in df.columns:
                columnsRename["Unnamed: 55"] = "SKU19"
            if 'Unnamed: 56' in df.columns:
                columnsRename["Unnamed: 56"] = "SKU20"

            df.rename(columns=columnsRename, inplace=True)
            # print(df.iloc[:8, :])
            # print(df.columns) #获取表头
            # df = df.drop([0], axis=0)
            # df = df.drop([1], axis=0)
            # df = df.drop([2], axis=0)
            # 删除data中索引为0和1的行
            df = df.drop(index=[0, 1, 2, 3])

            # 删除data中列名为“source”和“target”的列
            # df.drop(columns=['source', 'target'])
            # 参数axis为0表示在0轴（列）上搜索名为“姓名”的对象，然后删除对象“姓名”对应的行。
            # df.drop("姓名", axis=0)
            df = df.drop(index=df[(df.Owner == '.Mins')].index.tolist())
            # 会将标签重新从零开始顺序排序,使用参数设置drop=True删除旧的索引序列
            df = df.reset_index(drop=True)
            # print(df.shape)  # 获取行数列数
            # print(df.iloc[2188:, :])

            # print(index)
            # print(range(0,len(index)))

            # 参数axis为1表示在1轴（行）上搜索名为“姓名”的对象，然后删除对象“姓名”对应的列。
            # df.drop("姓名", axis=1)

            # # 插入列
            # df.insert(5, "Category", value='')
            # df.insert(6, "Category2", value='')
            # # 合并单元格
            # df['ItemNo_d'] = df['ItemNo_d'].ffill()
            # df['Item_d'] = df['Item_d'].ffill()
            # df['Version'] = df['Version'].ffill()
            # df['ReleaseDate'] = df['ReleaseDate'].ffill()

            # index = df[(df.Owner == '.Hrs')].index.tolist()
            # print(len(index))
            # # print(df[(df.Owner == '.Hrs')])
            # sub_Category = ['Pre-Installed App', 'WiGig Dock', 'USB Dock', 'Folio Case(Draft)', 'USB-C Dock', 'Thunderbolt Dock', 'Hybrid Dock',
            #                 'Power USB-C  Travel Hub & USB-C Mini dock', 'BT Folio Case', 'Lenovo 3-IN-1 Hub', 'USB-C Travel Hub Gen2',
            #                 'Lenovo USB-C 7-in-1 Hub']
            # for num in range(0, len(index)):
            #     # print(num)
            #     # print(data.loc[data['部门'] == 'A', ['姓名', '工资']])  # 部门为A，打印姓名和工资
            #     # print(data.loc[data['工资'] < 3000, ['姓名', '工资']])  # 查找工资小于3000的人
            #     # print(df['ItemNo_d'][index[num]])
            #     now_Category = '只记大类'
            #     if df['ItemNo_d'][index[num]] not in sub_Category:
            #         now_Category = df['ItemNo_d'][index[num]]
            #     if num != len(index)-1:
            #         df.loc[index[num]: index[num+1], 'Category'] = now_Category # 只记大类
            #         df.loc[index[num]: index[num + 1], 'Category2'] = df['ItemNo_d'][index[num]]
            #     else:#最后一个类别
            #         df.loc[index[num]:df.shape[0], 'Category'] = now_Category  # 只记大类
            #         df.loc[index[num]:df.shape[0], 'Category2'] = df['ItemNo_d'][index[num]]
            df = df.drop(index=df[(df.Owner == '.Hrs')].index.tolist())
            df = df.fillna('')  # 替换
            df = df.drop(index=df[(df.Owner == '')].index.tolist())
            # df = df.drop(index=df[(df.TestItems == '')].index.tolist())
            # print(df.head(8))
            # 会将标签重新从零开始顺序排序,使用参数设置drop=True删除旧的索引序列
            df = df.reset_index(drop=True)

            # phaseinexcel = pd.read_excel(src_file, header=1, sheet_name=int(sheetnum)).iloc[0:3, 1:3]  # ‘,’前面是行，后面是列，sheet_name指定sheet，可是是int第几个，可以是名称，header从第几行开始读取
            # print(phaseinexcel)
            # print(phaseinexcel.columns[0])
            Phase = ''
            # if "B(SDV)" in phaseinexcel.columns[0]:
            #     Phase = "B(FVT)"
            # elif "C(SIT)" in phaseinexcel.columns[0]:
            #     Phase = "C(SIT)"
            if sheetnum == '2':
                Phase = "B(SDV)"
            df.insert(0, "Customer", value=Customer)
            df.insert(1, "Phase", value=Phase)
            # wr_data = df.to_csv('out.csv')
            # 第一个参数为保存的文件名，注意，不能为空
            # sheet_name
            # 设置excel文件脚注
            # index = False
            # 这个意思是不将索引写入到文件中
            # print(df.iloc[1962:1965, :])
            df['ReleaseDate'] = df['ReleaseDate'].apply(
                lambda x: x.strftime('%Y-%m-%d') if 'datetime.datetime' in str(type(x)) else x)  # 批量类型转换
            print(df.shape)  # 获取行数列数
            with open('dataAIO.txt', 'w') as f:  # 设置文件对象
                print(df.shape, df.columns, file=f)
            df.to_excel('uploadAIO.xlsx', sheet_name="sheet1", index=False,
                        engine='xlsxwriter')  # engine默认是openpyxl， openpyxl生成的文件DDIS上传不了

            # write = pd.ExcelWriter("test.xlsx")  # 新建xlsx文件。
            # df.to_excel(write, sheet_name='Sheet1', index=False)  # 写入文件的Sheet1
            # write.save()  # 这里一定要保存

        if sheetnum == '3':
            df = pd.read_excel(src_file, header=5, sheet_name=int(sheetnum)).iloc[:,
                 2:]  # ‘,’前面是行，后面是列，sheet_name指定sheet，可是是int第几个，可以是名称，header从第几行开始读取
            # print(df.shape)#获取行数列数
            # if 'Unnamed: 26' in df.columns:
            #     # print(1)
            #     df = df.drop(labels='Unnamed: 26', axis=1)
            print(df.shape)  # 获取行数列数
            # # 显示所有列
            pd.set_option('display.max_columns', None)
            # # 显示所有行
            # pd.set_options('display.max_rows', None)
            # print(df.columns)
            # print(df.iloc[:1, :])
            # pprint.pprint(df)
            # sheet = pd.read_excel(src_file, sheet_name=0)
            # print(sheet)
            # print(df)
            # 转换字典
            # df_dict = df.to_dict(orient='records')
            # 转换列表
            # df_list = df.values
            # # pprint.pprint(df_list)
            # print(df_list[0])
            # 注意带上inplace=True参数用于更新作用于本数据集，而不是返回一个新的数据集。
            # df.rename(columns={'6-英语':'english'},inplace=True)
            # 如果需要重命名行索引，可以通过df.rename(index={‘原索引’:‘重命名索引’})的方式进行重命名。
            # 更多的，如果要重命名多个列，可以传入一个需要重命名的多个字典值，进行多个列的重命名。
            # df[['1-学号','2-姓名','3-年龄']].rename(columns={'1-学号':'ID','2-姓名':'name','3-年龄':'age'})
            columnsRename = {
                'Category': 'Category', 'Test Title': 'TestTitle', 'Sub test title': 'Subtesttitle',
                'Test Item': 'TestItem', 'Priority': 'Priority', 'Release Date': 'ReleaseDate', 'Owner ': 'Owner',
                # 'Version': 'Version',
                'Actual Time': 'AT_Totaltime',
                'Unnamed: 10': 'AT_AttendTime', 'Unnamed: 11': 'AT_UnattendTime', 'Unnamed: 12': 'AT_Automation',
                'DQMS Test Plan': 'DQMS_AttendTime', 'Unnamed: 14': 'DQMS_UnattendTime',
                'Test Units\n/Config': 'TestUnitsConfig', 'Smart Item': 'SmartItem',
                'AIO SW Test plan Matrix for Planning': 'Cusumer', 'Unnamed: 18': 'Commercial', 'Unnamed: 19': 'SDV',
                'Unnamed: 20': 'SIT', 'Unnamed: 21': 'Coverage',
                'Feature Support': 'FeatureSupport', 'Base time-support': 'Basetimesupport', 'TE': 'TE',
                'Schedule': 'Schedule',
                'Config-all test units': 'Configalltestunits', 'Config-all test time': 'Configalltesttime',
                'Config-Automation Item': 'ConfigAutomationItem', 'Config-Automation time': 'ConfigAutomationtime',
                'Config-Leverage Item': 'ConfigLeverageItem',
                'Config-Leverage time': 'ConfigLeveragetime', 'Config-Smart Item占总case比例': 'ConfigSmartItemper',
                'Config-Smart time': 'ConfigSmarttime',
                'Comments': 'Comments', 'Project test SKU-Optimize': 'ProjecttestSKUOptimize',
                'Attend time-Optimize': 'AttendtimeOptimize',
                'Planning after Optimize': 'SKU1', 'Unnamed: 38': 'SKU2', 'Unnamed: 39': 'SKU3', 'Unnamed: 40': 'SKU4',
                'Unnamed: 41': 'SKU5',
                'Unnamed: 42': 'SKU6', 'Unnamed: 43': 'SKU7', 'Unnamed: 44': 'SKU8', 'Unnamed: 45': 'SKU9',
                'Unnamed: 46': 'SKU10', 'Config-Retest Cycle': 'ConfigRetestCycle',
                'Config-Retest SKU': 'ConfigRetestSKU', 'Config-Retest time': 'ConfigRetesttime',
            }
            if 'Unnamed: 47' in df.columns:
                columnsRename["Unnamed: 47"] = "SKU11"
            if 'Unnamed: 48' in df.columns:
                columnsRename["Unnamed: 48"] = "SKU12"
            if 'Unnamed: 49' in df.columns:
                columnsRename["Unnamed: 49"] = "SKU13"
            if 'Unnamed: 50' in df.columns:
                columnsRename["Unnamed: 50"] = "SKU14"
            if 'Unnamed: 51' in df.columns:
                columnsRename["Unnamed: 51"] = "SKU15"
            if 'Unnamed: 52' in df.columns:
                columnsRename["Unnamed: 52"] = "SKU16"
            if 'Unnamed: 53' in df.columns:
                columnsRename["Unnamed: 53"] = "SKU17"
            if 'Unnamed: 54' in df.columns:
                columnsRename["Unnamed: 54"] = "SKU18"
            if 'Unnamed: 55' in df.columns:
                columnsRename["Unnamed: 55"] = "SKU19"
            if 'Unnamed: 56' in df.columns:
                columnsRename["Unnamed: 56"] = "SKU20"

            df.rename(columns=columnsRename, inplace=True)
            # print(df.iloc[:8, :])
            # print(df.columns) #获取表头
            # df = df.drop([0], axis=0)
            # df = df.drop([1], axis=0)
            # df = df.drop([2], axis=0)
            # 删除data中索引为0和1的行
            df = df.drop(index=[0, 1, 2, 3])

            # 删除data中列名为“source”和“target”的列
            # df.drop(columns=['source', 'target'])
            # 参数axis为0表示在0轴（列）上搜索名为“姓名”的对象，然后删除对象“姓名”对应的行。
            # df.drop("姓名", axis=0)
            df = df.drop(index=df[(df.Owner == '.Mins')].index.tolist())
            # 会将标签重新从零开始顺序排序,使用参数设置drop=True删除旧的索引序列
            df = df.reset_index(drop=True)
            # print(df.shape)  # 获取行数列数
            # print(df.iloc[2188:, :])

            # print(index)
            # print(range(0,len(index)))

            # 参数axis为1表示在1轴（行）上搜索名为“姓名”的对象，然后删除对象“姓名”对应的列。
            # df.drop("姓名", axis=1)

            # # 插入列
            # df.insert(5, "Category", value='')
            # df.insert(6, "Category2", value='')
            # # 合并单元格
            # df['ItemNo_d'] = df['ItemNo_d'].ffill()
            # df['Item_d'] = df['Item_d'].ffill()
            # df['Version'] = df['Version'].ffill()
            # df['ReleaseDate'] = df['ReleaseDate'].ffill()

            # index = df[(df.Owner == '.Hrs')].index.tolist()
            # print(len(index))
            # # print(df[(df.Owner == '.Hrs')])
            # sub_Category = ['Pre-Installed App', 'WiGig Dock', 'USB Dock', 'Folio Case(Draft)', 'USB-C Dock', 'Thunderbolt Dock', 'Hybrid Dock',
            #                 'Power USB-C  Travel Hub & USB-C Mini dock', 'BT Folio Case', 'Lenovo 3-IN-1 Hub', 'USB-C Travel Hub Gen2',
            #                 'Lenovo USB-C 7-in-1 Hub']
            # for num in range(0, len(index)):
            #     # print(num)
            #     # print(data.loc[data['部门'] == 'A', ['姓名', '工资']])  # 部门为A，打印姓名和工资
            #     # print(data.loc[data['工资'] < 3000, ['姓名', '工资']])  # 查找工资小于3000的人
            #     # print(df['ItemNo_d'][index[num]])
            #     now_Category = '只记大类'
            #     if df['ItemNo_d'][index[num]] not in sub_Category:
            #         now_Category = df['ItemNo_d'][index[num]]
            #     if num != len(index)-1:
            #         df.loc[index[num]: index[num+1], 'Category'] = now_Category # 只记大类
            #         df.loc[index[num]: index[num + 1], 'Category2'] = df['ItemNo_d'][index[num]]
            #     else:#最后一个类别
            #         df.loc[index[num]:df.shape[0], 'Category'] = now_Category  # 只记大类
            #         df.loc[index[num]:df.shape[0], 'Category2'] = df['ItemNo_d'][index[num]]
            df = df.drop(index=df[(df.Owner == '.Hrs')].index.tolist())
            df = df.fillna('')  # 替换
            df = df.drop(index=df[(df.Owner == '')].index.tolist())
            # df = df.drop(index=df[(df.TestItems == '')].index.tolist())
            # print(df.head(8))
            # 会将标签重新从零开始顺序排序,使用参数设置drop=True删除旧的索引序列
            df = df.reset_index(drop=True)

            # phaseinexcel = pd.read_excel(src_file, header=1, sheet_name=int(sheetnum)).iloc[0:3, 1:3]  # ‘,’前面是行，后面是列，sheet_name指定sheet，可是是int第几个，可以是名称，header从第几行开始读取
            # print(phaseinexcel)
            # print(phaseinexcel.columns[0])
            Phase = ''
            # if "B(SDV)" in phaseinexcel.columns[0]:
            #     Phase = "B(FVT)"
            # elif "C(SIT)" in phaseinexcel.columns[0]:
            #     Phase = "C(SIT)"
            if sheetnum == '3':
                Phase = "C(SIT)"
            df.insert(0, "Customer", value=Customer)
            df.insert(1, "Phase", value=Phase)
            # wr_data = df.to_csv('out.csv')
            # 第一个参数为保存的文件名，注意，不能为空
            # sheet_name
            # 设置excel文件脚注
            # index = False
            # 这个意思是不将索引写入到文件中
            # print(df.iloc[1962:1965, :])

            df['ReleaseDate'] = df['ReleaseDate'].apply(
                lambda x: x.strftime('%Y-%m-%d') if 'datetime.datetime' in str(type(x)) else x)  # 批量类型转换
            # df['ReleaseDate'] = df['ReleaseDate'].apply(lambda x: print(x) if 'str' in str(type(x)) else print(type(x)))
            print(df.shape)  # 获取行数列数
            with open('dataAIO.txt', 'w') as f:  # 设置文件对象
                print(df.shape, df.columns, file=f)
            df.to_excel('uploadAIO.xlsx', sheet_name="sheet1", index=False,
                        engine='xlsxwriter')  # engine默认是openpyxl， openpyxl生成的文件DDIS上传不了

            # write = pd.ExcelWriter("test.xlsx")  # 新建xlsx文件。
            # df.to_excel(write, sheet_name='Sheet1', index=False)  # 写入文件的Sheet1
            # write.save()  # 这里一定要保存

        if sheetnum == '4':
            df = pd.read_excel(src_file, header=5, sheet_name=int(sheetnum)).iloc[:,
                 2:]  # ‘,’前面是行，后面是列，sheet_name指定sheet，可是是int第几个，可以是名称，header从第几行开始读取
            # print(df.shape)#获取行数列数
            # if 'Unnamed: 26' in df.columns:
            #     # print(1)
            #     df = df.drop(labels='Unnamed: 26', axis=1)
            print(df.shape)  # 获取行数列数
            # # 显示所有列
            pd.set_option('display.max_columns', None)
            # # 显示所有行
            # pd.set_options('display.max_rows', None)
            # print(df.columns)
            # print(df.iloc[:1, :])
            # pprint.pprint(df)
            # sheet = pd.read_excel(src_file, sheet_name=0)
            # print(sheet)
            # print(df)
            # 转换字典
            # df_dict = df.to_dict(orient='records')
            # 转换列表
            # df_list = df.values
            # # pprint.pprint(df_list)
            # print(df_list[0])
            # 注意带上inplace=True参数用于更新作用于本数据集，而不是返回一个新的数据集。
            # df.rename(columns={'6-英语':'english'},inplace=True)
            # 如果需要重命名行索引，可以通过df.rename(index={‘原索引’:‘重命名索引’})的方式进行重命名。
            # 更多的，如果要重命名多个列，可以传入一个需要重命名的多个字典值，进行多个列的重命名。
            # df[['1-学号','2-姓名','3-年龄']].rename(columns={'1-学号':'ID','2-姓名':'name','3-年龄':'age'})
            columnsRename = {
                'Category': 'Category', 'Test Title': 'TestTitle', 'Sub test title': 'Subtesttitle',
                'Test Item': 'TestItem', 'Priority': 'Priority', 'Release Date': 'ReleaseDate', 'Owner ': 'Owner',
                # 'Version': 'Version',
                'Actual Time': 'AT_Totaltime',
                'Unnamed: 10': 'AT_AttendTime', 'Unnamed: 11': 'AT_UnattendTime', 'Unnamed: 12': 'AT_Automation',
                'DQMS Test Plan': 'DQMS_AttendTime', 'Unnamed: 14': 'DQMS_UnattendTime',
                'Test Units\n/Config': 'TestUnitsConfig', 'Smart Item': 'SmartItem',
                'AIO SW Test plan Matrix for Planning': 'Cusumer', 'Unnamed: 18': 'Commercial', 'Unnamed: 19': 'SDV',
                'Unnamed: 20': 'SIT', 'Unnamed: 21': 'Coverage',
                'Feature Support': 'FeatureSupport', 'Base time-support': 'Basetimesupport', 'TE': 'TE',
                'Schedule': 'Schedule',
                'Config-all test units': 'Configalltestunits', 'Config-all test time': 'Configalltesttime',
                'Config-Automation Item': 'ConfigAutomationItem', 'Config-Automation time': 'ConfigAutomationtime',
                'Config-Leverage Item': 'ConfigLeverageItem',
                'Config-Leverage time': 'ConfigLeveragetime', 'Config-Smart Item占总case比例': 'ConfigSmartItemper',
                'Config-Smart time': 'ConfigSmarttime',
                'Comments': 'Comments', 'Project test SKU-Optimize': 'ProjecttestSKUOptimize',
                'Attend time-Optimize': 'AttendtimeOptimize',
                'Planning after Optimize': 'SKU1', 'Unnamed: 38': 'SKU2', 'Unnamed: 39': 'SKU3', 'Unnamed: 40': 'SKU4',
                'Unnamed: 41': 'SKU5',
                'Unnamed: 42': 'SKU6', 'Unnamed: 43': 'SKU7', 'Unnamed: 44': 'SKU8', 'Unnamed: 45': 'SKU9',
                'Unnamed: 46': 'SKU10', 'Config-Retest Cycle': 'ConfigRetestCycle',
                'Config-Retest SKU': 'ConfigRetestSKU', 'Config-Retest time': 'ConfigRetesttime',
            }
            if 'Unnamed: 47' in df.columns:
                columnsRename["Unnamed: 47"] = "SKU11"
            if 'Unnamed: 48' in df.columns:
                columnsRename["Unnamed: 48"] = "SKU12"
            if 'Unnamed: 49' in df.columns:
                columnsRename["Unnamed: 49"] = "SKU13"
            if 'Unnamed: 50' in df.columns:
                columnsRename["Unnamed: 50"] = "SKU14"
            if 'Unnamed: 51' in df.columns:
                columnsRename["Unnamed: 51"] = "SKU15"
            if 'Unnamed: 52' in df.columns:
                columnsRename["Unnamed: 52"] = "SKU16"
            if 'Unnamed: 53' in df.columns:
                columnsRename["Unnamed: 53"] = "SKU17"
            if 'Unnamed: 54' in df.columns:
                columnsRename["Unnamed: 54"] = "SKU18"
            if 'Unnamed: 55' in df.columns:
                columnsRename["Unnamed: 55"] = "SKU19"
            if 'Unnamed: 56' in df.columns:
                columnsRename["Unnamed: 56"] = "SKU20"

            df.rename(columns=columnsRename, inplace=True)
            # print(df.iloc[:8, :])
            # print(df.columns) #获取表头
            # df = df.drop([0], axis=0)
            # df = df.drop([1], axis=0)
            # df = df.drop([2], axis=0)
            # 删除data中索引为0和1的行
            df = df.drop(index=[0, 1, 2, 3])

            # 删除data中列名为“source”和“target”的列
            # df.drop(columns=['source', 'target'])
            # 参数axis为0表示在0轴（列）上搜索名为“姓名”的对象，然后删除对象“姓名”对应的行。
            # df.drop("姓名", axis=0)
            df = df.drop(index=df[(df.Owner == '.Mins')].index.tolist())
            # 会将标签重新从零开始顺序排序,使用参数设置drop=True删除旧的索引序列
            df = df.reset_index(drop=True)
            # print(df.shape)  # 获取行数列数
            # print(df.iloc[2188:, :])

            # print(index)
            # print(range(0,len(index)))

            # 参数axis为1表示在1轴（行）上搜索名为“姓名”的对象，然后删除对象“姓名”对应的列。
            # df.drop("姓名", axis=1)

            # # 插入列
            # df.insert(5, "Category", value='')
            # df.insert(6, "Category2", value='')
            # # 合并单元格
            # df['ItemNo_d'] = df['ItemNo_d'].ffill()
            # df['Item_d'] = df['Item_d'].ffill()
            # df['Version'] = df['Version'].ffill()
            # df['ReleaseDate'] = df['ReleaseDate'].ffill()

            # index = df[(df.Owner == '.Hrs')].index.tolist()
            # print(len(index))
            # # print(df[(df.Owner == '.Hrs')])
            # sub_Category = ['Pre-Installed App', 'WiGig Dock', 'USB Dock', 'Folio Case(Draft)', 'USB-C Dock', 'Thunderbolt Dock', 'Hybrid Dock',
            #                 'Power USB-C  Travel Hub & USB-C Mini dock', 'BT Folio Case', 'Lenovo 3-IN-1 Hub', 'USB-C Travel Hub Gen2',
            #                 'Lenovo USB-C 7-in-1 Hub']
            # for num in range(0, len(index)):
            #     # print(num)
            #     # print(data.loc[data['部门'] == 'A', ['姓名', '工资']])  # 部门为A，打印姓名和工资
            #     # print(data.loc[data['工资'] < 3000, ['姓名', '工资']])  # 查找工资小于3000的人
            #     # print(df['ItemNo_d'][index[num]])
            #     now_Category = '只记大类'
            #     if df['ItemNo_d'][index[num]] not in sub_Category:
            #         now_Category = df['ItemNo_d'][index[num]]
            #     if num != len(index)-1:
            #         df.loc[index[num]: index[num+1], 'Category'] = now_Category # 只记大类
            #         df.loc[index[num]: index[num + 1], 'Category2'] = df['ItemNo_d'][index[num]]
            #     else:#最后一个类别
            #         df.loc[index[num]:df.shape[0], 'Category'] = now_Category  # 只记大类
            #         df.loc[index[num]:df.shape[0], 'Category2'] = df['ItemNo_d'][index[num]]
            df = df.drop(index=df[(df.Owner == '.Hrs')].index.tolist())
            df = df.fillna('')  # 替换
            df = df.drop(index=df[(df.Owner == '')].index.tolist())
            # df = df.drop(index=df[(df.TestItems == '')].index.tolist())
            # print(df.head(8))
            # 会将标签重新从零开始顺序排序,使用参数设置drop=True删除旧的索引序列
            df = df.reset_index(drop=True)

            # phaseinexcel = pd.read_excel(src_file, header=1, sheet_name=int(sheetnum)).iloc[0:3, 1:3]  # ‘,’前面是行，后面是列，sheet_name指定sheet，可是是int第几个，可以是名称，header从第几行开始读取
            # print(phaseinexcel)
            # print(phaseinexcel.columns[0])
            Phase = ''
            # if "B(SDV)" in phaseinexcel.columns[0]:
            #     Phase = "B(FVT)"
            # elif "C(SIT)" in phaseinexcel.columns[0]:
            #     Phase = "C(SIT)"
            if sheetnum == '4':
                Phase = "EELP+"
            df.insert(0, "Customer", value=Customer)
            df.insert(1, "Phase", value=Phase)
            # wr_data = df.to_csv('out.csv')
            # 第一个参数为保存的文件名，注意，不能为空
            # sheet_name
            # 设置excel文件脚注
            # index = False
            # 这个意思是不将索引写入到文件中
            # print(df.iloc[1962:1965, :])
            df['ReleaseDate'] = df['ReleaseDate'].apply(
                lambda x: x.strftime('%Y-%m-%d') if 'datetime.datetime' in str(type(x)) else x)  # 批量类型转换
            print(df.shape)  # 获取行数列数
            with open('dataAIO.txt', 'w') as f:  # 设置文件对象
                print(df.shape, df.columns, file=f)
            df.to_excel('uploadAIO.xlsx', sheet_name="sheet1", index=False,
                        engine='xlsxwriter')  # engine默认是openpyxl， openpyxl生成的文件DDIS上传不了

            # write = pd.ExcelWriter("test.xlsx")  # 新建xlsx文件。
            # df.to_excel(write, sheet_name='Sheet1', index=False)  # 写入文件的Sheet1
            # write.save()  # 这里一定要保存

        self.enable_button_signal.emit()
        self.infobox_signal.emit('%s-%s模板转换已完成' % (self.Customer, self.Phase))



from PyQt5.QtCore import Qt
try:
    if __name__ == '__main__':
        ######使用下面的方式一定程度上可以解决界面模糊问题--解决电脑缩放比例问题
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

        # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

        # 在主函数入口之前加入上面的设置即可解决
        app = QApplication(sys.argv)
        C = CheckFun()
        C.show()
        sys.exit(app.exec())

except Exception as e:
    with open('error.txt', 'w') as f:  # 设置文件对象
        print(e, file=f)
