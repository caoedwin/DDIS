from django.shortcuts import render
from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from TestPlanME.models import TestPlanME,TestProjectME,TestItemME
from TestPlanSW.models import TestPlanSW,TestProjectSW,TestItemSW,RetestItemSW
from app01.models import UserInfo
import datetime,json,simplejson

# Create your views here.
def TestPlanSW_Edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Edit"
    # MockData = [
    #             # {"caseid": "Basic", "contents": [
    #             #     {"id": 20191210, "caseid": "BFA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "unattendedtime": 695,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191211, "caseid": "BFA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 400, "unattendedtime": 400,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191212, "caseid": "BFA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 500, "unattendedtime": 500,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191213, "caseid": "BFA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 600, "unattendedtime": 600,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191214, "caseid": "BFA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 700, "unattendedtime": 700,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191215, "caseid": "BFA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 800, "unattendedtime": 800,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     ]},
    #             # {"caseid": "Interaction", "contents": [
    #             #     {"id": 20191216, "caseid": "IAA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 10,
    #             #      "unattendedtime": 10, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191217, "caseid": "IAA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 20,
    #             #      "unattendedtime": 20, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191218, "caseid": "IAA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 30,
    #             #      "unattendedtime": 30, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191219, "caseid": "IAA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 40,
    #             #      "unattendedtime": 40, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191220, "caseid": "IAA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 50,
    #             #      "unattendedtime": 50, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191221, "caseid": "IAA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 60,
    #             #      "unattendedtime": 60, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     ]},
    #             # {"caseid": "Connectivity", "contents": [
    #             #     {"id": 20191222, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191223, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191224, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191225, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191226, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191227, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     ]},
    #             # {"caseid": "Process and Stroage", "contents": [
    #             #     {"id": 20191228, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191229, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191230, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191231, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191232, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191233, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Performance", "contents": [
    #             #     {"id": 20191234, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191235, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191236, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191237, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191238, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191239, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Game Test", "contents": [
    #             #     {"id": 20191240, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191241, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191242, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191243, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191244, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191245, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Stress", "contents": [
    #             #     {"id": 20191246, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191247, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191248, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191249, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191250, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191251, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Application", "contents": [
    #             #     {"id": 20191252, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191253, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191254, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191255, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191256, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191257, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Compal internal", "contents": [
    #             #     {"id": 20191258, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191259, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191260, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191261, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191262, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191263, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Game unique", "contents": [
    #             #     {"id": 20191264, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191265, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191266, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191267, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191268, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191269, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Linux and DOS", "contents": [
    #             #     {"id": 20191270, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191271, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191272, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191273, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191274, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191275, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Accessories", "contents": [
    #             #     {"id": 20191276, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191277, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191278, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191279, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191280, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191281, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Gaming Unique", "contents": [
    #             #     {"id": 20191282, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191283, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191284, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191285, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191286, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191287, "caseid": "PFA005_15", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             ]
    # newMockData = [
    #                #  {"caseid": "Game unique", "contents": [
    #                #      {"id": 20191264, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191265, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191266, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191267, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191268, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191269, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #  ]},
    #                # {"caseid": "Linux and DOS", "contents": [
    #                #     {"id": 20191270, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191271, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191272, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191273, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191274, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191275, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                # ]},
    #                # {"caseid": "Accessories", "contents": [
    #                #     {"id": 20191276, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191277, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191278, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191279, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191280, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191281, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                # ]},
    #                # {"caseid": "Gaming Unique", "contents": [
    #                #     {"id": 20191282, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191283, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191284, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191285, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191286, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191287, "caseid": "PFA005_15", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                # ]},
    #                ]
    newContents = [
        # {"id": 20191264, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "testitem":"","version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191265, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191266, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191267, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191268, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 1,
        #  "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191269, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 1,
        #  "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
    ]
    title = [
             # {"caseid": "Basic", 'hasChildren': 'true'},
             # {"caseid": "Interaction", 'hasChildren': 'true'},
             # {"caseid": "Connectivity", 'hasChildren': 'true'},
             # {"caseid": "Process and Stroage", 'hasChildren': 'true'},
             # {"caseid": "Performance", 'hasChildren': 'true'},
             # {"caseid": "Game Test", 'hasChildren': 'true'},
             # {"caseid": "Stress", 'hasChildren': 'true'},
             # {"caseid": "Application", 'hasChildren': 'true'},
             # {"caseid": "Compal internal", 'hasChildren': 'true'},
             # {"caseid": "Game unique", 'hasChildren': 'true'},
             # {"caseid": "Linux and DOS", 'hasChildren': 'true'},
             # {"caseid": "Accessories", 'hasChildren': 'true'},
             # {"caseid": "Gaming Unique", 'hasChildren': 'true'},
             ]
    SKU = [
           # {"skuNo": "SKU1", "VGA": "UMA", "CPU": "i3-8145U"},
           # {"skuNo": "SKU2", "VGA": "N17S-G2-A1", "CPU": "i5-8265U"},
           # {"skuNo": "SKU2", "VGA": "UMA", "CPU": "i5-8265U"},
           # {"skuNo": "SKU3", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"},
           # {"skuNo": "SKU4", "VGA": "Picasso", "CPU": "i7-8565U"}, {"skuNo": "SKU5", "VGA": "UMA", "CPU": "i7-8565U"},
           # {"skuNo": "SKU6", "VGA": "N17S-G2-A1", "CPU": "i7-8565U"},
           # {"skuNo": "SKU7", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"}
    ]
    combine = {
        # "C38(NB)": [{"project": "ELMV2", "phase": [0, 1, 2, 3]}, {"project": "FLY00", "phase": [2, 3]},
        #             {"project": "ELZP5", "phase": [1]}, {"project": "ELZP7", "phase": [1, 2, 3]}],
        # "C38(AIO)": [{"project": "FLMS0", "phase": [1, 2, 3]}, {"project": "FLMS1", "phase": [1, 2, 3]},
        #              {"project": "FLMS2", "phase": [1, 2, 3]}],
        # "A39": [{"project": "DLAE1", "phase": [1, 2, 3]}, {"project": "DLAE2", "phase": [1, 2, 3]},
        #         {"project": "DLAE3", "phase": [1, 2, 3]}],
        # "Other": [{"project": "OTHER", "phase": [1, 2, 3]}]
    }
    Customer_list = TestProjectSW.objects.all().values('Customer').distinct().order_by('Customer')

    for i in Customer_list:
        Customerlist = []
        for j in TestProjectSW.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            phaselist = []
            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            for m in TestProjectSW.objects.filter(**dic).values('Phase').distinct().order_by('Phase'):

                if m['Phase'] == "B(FVT)":
                    PhaseValue = 0
                if m['Phase'] == "C(SIT)":
                    PhaseValue = 1
                if m['Phase'] == "FFRT":
                    PhaseValue = 2
                if m['Phase'] == "Others":
                    PhaseValue = 3
                phaselist.append(PhaseValue)
            Projectinfo['phase'] = phaselist
            Projectinfo['project'] = j['Project']
            Customerlist.append(Projectinfo)
        combine[i['Customer']] = Customerlist
    # print (request.method)
    # print(request.GET,request.GET.get("action"),request.POST)
    # print(request.body)
    if request.method == "GET":
        if request.GET.get("action") == "first":
            return HttpResponse(json.dumps(combine), content_type="application/json")
        elif request.GET.get("action") == "search":
            # if request.GET.get("customer") == "C38(NB)":
                Customer = request.GET.get('customer')
                Project = request.GET.get('project')
                Phase = request.GET.get('phase')
                # print(type(Phase))
                if Phase == '0':
                    Phase = 'B(FVT)'
                if Phase == '1':
                    Phase = 'C(SIT)'
                if Phase == '2':
                    Phase = 'FFRT'
                if Phase == '3':
                    Phase = 'Others'
                dic_Item=     {'Customer': Customer, 'Phase': Phase}
                dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
                # print(dic_Project)
                Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
                # print(Projectinfos.Owner.all())
                # print(Projectinfos)
                canEdit = 0
                current_user = request.session.get('user_name')
                if Projectinfos:
                    for i in Projectinfos.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if i.username == current_user:
                            canEdit = 1
                            break
                    SKUlist=[Projectinfos.SKU1,Projectinfos.SKU2,Projectinfos.SKU3,Projectinfos.SKU4,Projectinfos.SKU5,
                              Projectinfos.SKU6,Projectinfos.SKU7,Projectinfos.SKU8,Projectinfos.SKU9,Projectinfos.SKU10,
                              Projectinfos.SKU11,Projectinfos.SKU12,Projectinfos.SKU13,Projectinfos.SKU14,Projectinfos.SKU15,
                              Projectinfos.SKU16,Projectinfos.SKU17,Projectinfos.SKU18,Projectinfos.SKU19,Projectinfos.SKU20]
                    n=1
                    for i in SKUlist:
                        if i:
                            SKUno='SKU%s'%n
                            SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
                            n+=1
                # print(SKU)
                if canEdit:
                    itemlist = []
                    for i in TestItemSW.objects.filter(Customer=Customer,Phase=Phase):
                        itemlist.append(i.id)
                    # print (itemlist,'yyy')
                    existitem = []
                    for i in Projectinfos.testplansw_set.all():
                        existitem.append(i.Items.id)
                    # print(existitem)
                    for i in itemlist:
                        if i in existitem:
                            continue
                        else:
                            # print(TestProjectSW.objects.filter(**dic_Project).first())
                            TestPlanSW.objects.create(Items=TestItemSW.objects.get(id=i),
                                                      Projectinfo=TestProjectSW.objects.filter(**dic_Project).first())
                    # print (TestItemSW.objects.all().values('Category2').distinct().count())
                m=0
                for i in TestItemSW.objects.filter(**dic_Item).values('Category2').distinct():
                    # print(type(i),i)
                    title.append({"caseid": i['Category2'], 'hasChildren': 'true'})
                    m+=1
                dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
                if RetestItemSW.objects.filter(**dic_Project).first():
                    title.append({"caseid": "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution’s issue ) for full function test", 'hasChildren': 'true'})
                # print(title)


                updateData = {
                    "MockData": title,
                    "SKU": SKU,
                    "selectMsg": combine,
                    "canEdit": canEdit
                }
                return HttpResponse(json.dumps(updateData), content_type="application/json")
            # if request.GET.get("customer") == "C38(AIO)":
            #     updateData = {
            #         "MockData": title1,
            #         "SKU": SKU,
            #         "selectMsg": combine,
            #         "canEdit": 1
            #     }
            #     return HttpResponse(json.dumps(updateData), content_type="application/json")
            # if request.GET.get("customer") == "A39":
            #     updateData = {
            #         "MockData": title,
            #         "SKU": SKU,
            #         "selectMsg": combine,
            #         "canEdit": 1
            #     }
            # return HttpResponse(json.dumps(updateData), content_type="application/json")
        elif request.GET.get("action") == "getContent":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            Category2=request.GET.get('contents')
            # print(Category2)
            # print(type(Phase))
            if Phase == '0':
                Phase = 'B(FVT)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'FFRT'
            if Phase == '3':
                Phase = 'Others'
            dicItem={'Customer': Customer, 'Phase': Phase,'Category2':Category2}
            # print(dicItem)
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            if request.GET.get("contents") == "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution’s issue ) for full function test":
                RetestItemSWinfo=RetestItemSW.objects.filter(**dic_Project)
                # print('Retest')
                if RetestItemSWinfo:
                    for i in RetestItemSWinfo:
                        planOptimize=[]
                        SKUlist = [i.SKU1, i.SKU2, i.SKU3, i.SKU4,i.SKU5,
                                   i.SKU6, i.SKU7, i.SKU8, i.SKU9,i.SKU10,
                                   i.SKU11, i.SKU12, i.SKU13, i.SKU14,i.SKU15,
                                   i.SKU16, i.SKU17, i.SKU18, i.SKU19,i.SKU20]

                        for j in SKUlist:
                            if j:
                                planOptimize.append(j)
                            # print(planOptimize)
                        newContents.append(
                            {  # Reitem
                                "id": i.id, "caseid": i.ItemNo_d, "casename": i.Item_d,
                                "testitem": i.TestItems,
                                "version": i.Version,
                                "releasedate": i.ReleaseDate, "owner": i.Owner,
                                "priority": i.Priority,
                                # TDMSTotalTime前端直接后两项加总
                                "basetime": i.BaseTime,
                                "unattendedtime": i.TDMSUnattendedTime,
                                "basetimeA": i.BaseAotomationTime1SKU,
                                "chramshell": i.Chramshell, "conver_NB": i.ConvertibaleNBMode,
                                "conver_Yoga": i.ConvertibaleYogaPadMode,
                                "detach_Pad": i.DetachablePadMode, "detach_W": i.DetachableWDockmode,
                                "PhaseF": i.PhaseFVT, "PhaseS": i.PhaseSIT, 'PhaseFFRT': i.PhaseFFRT,
                                "coverage": i.Coverage,
                                'FS': i.FeatureSupport, 'TE': i.TE, 'schedule': i.Schedule,
                                'starttime': i.ProjectTestSKUfollowMatrix, 'conAitem': i.ConfigAutomationItem,
                                'conLitem': i.ConfigLeverageItem, 'comments1': i.CommentsLeverage,
                                'conSitem': i.ConfigSmartItem,
                                'comments2': i.CommentsSmart, "planOptimize": planOptimize, 'CRC': i.ConfigRetestCycle,
                                'CRS': i.ConfigRetestSKU, 'CRT': i.ConfigRetestTime,
                                # no need edit
                                'BTS':i.BaseTimeSupport,'TFC':i.TimewConfigFollowmatrix,'conAtime':i.ConfigAutomationTime,'conLtime':i.ConfigLeverageTime,
                                'conSitemInAll':i.ConfigSmartItem,'conStime':i.ConfigSmartTime,'proTS':i.ProjectTestSKUOptimize,'ATO':i.AttendTimeOptimize
                            })
                    # print(newContents)
            else:
                # print('Others')
                Iteminfos=TestItemSW.objects.filter(**dicItem)
                Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
                # print(Projectinfos.Owner.all())
                # print(Iteminfos)
                # print(Projectinfos)
                if Projectinfos:
                    x=0
                    for h in Iteminfos:
                        for i in TestPlanSW.objects.filter(Items=h,Projectinfo=Projectinfos):
                            x+=1
                            # print(i,type(i))
                            # print(i.id)
                            planOptimize = []
                            SKUlist = [i.SKU1, i.SKU2, i.SKU3, i.SKU4, i.SKU5,
                                       i.SKU6, i.SKU7, i.SKU8, i.SKU9, i.SKU10,
                                       i.SKU11, i.SKU12, i.SKU13, i.SKU14, i.SKU15,
                                       i.SKU16, i.SKU17, i.SKU18, i.SKU19, i.SKU20]

                            for j in SKUlist:
                                if j:
                                    planOptimize.append(j)
                                # print(planOptimize)
                            # print(i.ConfigSmartItemPer,i.ConfigSmartTime)
                            newContents.append(
                                {#item
                                    "id": i.id, "caseid": i.Items.ItemNo_d, "casename": i.Items.Item_d, "testitem": i.Items.TestItems,
                                 "version": i.Items.Version,
                                 "releasedate": i.Items.ReleaseDate, "owner": i.Items.Owner, "priority": i.Items.Priority,
                                    #TDMSTotalTime前端直接后两项加总
                                 "basetime": i.Items.BaseTime,
                                 "unattendedtime": i.Items.TDMSUnattendedTime, "basetimeA": i.Items.BaseAotomationTime1SKU,
                                 "chramshell": i.Items.Chramshell, "conver_NB": i.Items.ConvertibaleNBMode,
                                 "conver_Yoga": i.Items.ConvertibaleYogaPadMode,
                                 "detach_Pad": i.Items.DetachablePadMode, "detach_W": i.Items.DetachableWDockmode,
                                 "PhaseF": i.Items.PhaseFVT, "PhaseS": i.Items.PhaseSIT, 'PhaseFFRT': i.Items.PhaseFFRT,
                                 "coverage": i.Items.Coverage,
                                    #plan
                                 'FS':i.FeatureSupport,'TE':i.TE,'schedule':i.Schedule,
                                 'starttime':i.ProjectTestSKUfollowMatrix,'conAitem':i.ConfigAutomationItem,
                                 'conLitem':i.ConfigLeverageItem,'comments1':i.CommentsLeverage,'conSitem':i.ConfigSmartItem,
                                 'comments2':i.CommentsSmart,"planOptimize": planOptimize,'CRC':i.ConfigRetestCycle,'CRS':i.ConfigRetestSKU,'CRT':i.ConfigRetestTime,
                                    # no need edit
                                    'BTS': i.BaseTimeSupport, 'TFC': i.TimewConfigFollowmatrix,
                                    'CAT': i.ConfigAutomationTime, 'CLT': i.ConfigLeverageTime,
                                    'conSitemInAll': i.ConfigSmartItemPer, 'CST': i.ConfigSmartTime,
                                    'proTS': i.ProjectTestSKUOptimize, 'ATO': i.AttendTimeOptimize
                                })
                    # print(newContents)
                    # print(x)
            # print(newContents)
            return HttpResponse(json.dumps(newContents), content_type="application/json")
            # if request.GET.get("contents") == "Basic":
            #     return HttpResponse(json.dumps(newContents), content_type="application/json")
            # if request.GET.get("contents") == "Interaction":
            #     return HttpResponse(json.dumps(newContents1), content_type="application/json")
            # if request.GET.get("contents") == "Connectivity":
            #     return HttpResponse(json.dumps(newContents2), content_type="application/json")

    if request.method == "POST":
        # print(request.body)
        # print(json.loads(request.body))
        responseData = json.loads(request.body)
        #excel
        if 'ExcelData' in responseData.keys():
            xlsxlist = json.loads(responseData['ExcelData'])
            if responseData:
                # print(responseData['Projectinfo'][2])
                if responseData['phase'] == 0:
                    Phase = 'B(FVT)'
                if responseData['phase'] == 1:
                    Phase = 'C(SIT)'
                if responseData['phase'] == 2:
                    Phase = 'FFRT'
                if responseData['phase'] == 3:
                    Phase = 'Others'
                dic_Project = {'Customer': responseData['customer'],
                               'Project': responseData['project'], 'Phase': Phase}
                Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
                # print(dic_Project)
                item_nodata = [{'Customer':'Customer','Phase':'Phase','ItemNo_d': 'Case_ID', 'Item_d': 'Case_Name','TestItems':'Test_Items'}]
                for i in xlsxlist:
                    # print(i)
                    #RetestFFRT
                    if i['Category2']== "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution’s issue ) for full function test":
                        # print('yes')
                        # print(i['ItemNo_d'], i['Item_d'], i['TestItems'])
                        if 'ItemNo_d' in i.keys() and 'Item_d' in i.keys() and 'TestItems' in i.keys():

                            # print('yeah')
                            check_dicRetestplan= {'Customer':responseData['customer'], 'Project':responseData['project'],
                              'Phase':Phase,'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d'],'TestItems':i['TestItems'],
                                                  'Projectinfo':TestProjectSW.objects.get(**dic_Project)}

                            # print(check_dicRetestplan)

                            editplan = RetestItemSW.objects.filter(**check_dicRetestplan).first()

                            # print(type(editplan),editplan)
                            # edit
                            if editplan:
                                # print('edit')
                                editplan.Customer=responseData['customer']
                                editplan.Phase=Phase
                                editplan.Project=responseData['project']
                                editplan.ItemNo_d=i['ItemNo_d']
                                editplan.Item_d=i['Item_d']
                                editplan.TestItems=i['TestItems']
                                if 'Category' in i.keys():
                                    editplan.Category = i['Category']
                                if 'Category2' in i.keys():
                                    editplan.Category2 = i['Category2']
                                if 'Version' in i.keys():
                                    editplan.Version = i['Version']
                                if 'ReleaseDate' in i.keys():
                                    editplan.ReleaseDate = i['ReleaseDate']
                                if 'Owner' in i.keys():
                                    editplan.Owner = i['Owner']
                                if 'Priority' in i.keys():
                                    editplan.Priority = i['Priority']
                                if 'TDMSTotalTime' in i.keys():
                                    editplan.TDMSTotalTime = i['TDMSTotalTime']
                                if 'BaseTime' in i.keys():
                                    editplan.BaseTime = i['BaseTime']
                                if 'TDMSUnattendedTime' in i.keys():
                                    editplan.TDMSUnattendedTime = i['TDMSUnattendedTime']
                                if 'BaseAotomationTime1SKU' in i.keys():
                                    editplan.BaseAotomationTime1SKU = i['BaseAotomationTime1SKU']
                                if 'Chramshell' in i.keys():
                                    editplan.Chramshell = i['Chramshell']
                                if 'ConvertibaleNBMode' in i.keys():
                                    editplan.ConvertibaleNBMode = i['ConvertibaleNBMode']
                                if 'ConvertibaleYogaPadMode' in i.keys():
                                    editplan.ConvertibaleYogaPadMode = i['ConvertibaleYogaPadMode']
                                if 'DetachablePadMode' in i.keys():
                                    editplan.DetachablePadMode = i['DetachablePadMode']
                                if 'DetachableWDockmode' in i.keys():
                                    editplan.DetachableWDockmode = i['DetachableWDockmode']
                                if 'PhaseFVT' in i.keys():
                                    editplan.PhaseFVT = i['PhaseFVT']
                                if 'PhaseSIT' in i.keys():
                                    editplan.PhaseSIT = i['PhaseSIT']
                                if 'PhaseFFRT' in i.keys():
                                    editplan.PhaseFFRT = i['PhaseFFRT']
                                if 'Coverage' in i.keys():
                                    editplan.Coverage = i['Coverage']

                                if 'FeatureSupport' in i.keys():
                                    editplan.FeatureSupport = i['FeatureSupport']
                                if 'BaseTimeSupport' in i.keys():
                                    editplan.BaseTimeSupport = i['BaseTimeSupport']
                                if 'TE' in i.keys():
                                    editplan.TE = i['TE']
                                if 'Schedule' in i.keys():
                                    editplan.Schedule = i['Schedule']
                                if 'ProjectTestSKUfollowMatrix' in i.keys():
                                    editplan.ProjectTestSKUfollowMatrix = i['ProjectTestSKUfollowMatrix']
                                if 'TimewConfigFollowmatrix' in i.keys():
                                    editplan.TimewConfigFollowmatrix = i['TimewConfigFollowmatrix']
                                if 'ConfigAutomationItem' in i.keys():
                                    editplan.ConfigAutomationItem = i['ConfigAutomationItem']
                                if 'ConfigAutomationTime' in i.keys():
                                    editplan.ConfigAutomationTime = i['ConfigAutomationTime']
                                if 'ConfigLeverageItem' in i.keys():
                                    editplan.ConfigLeverageItem = i['ConfigLeverageItem']
                                if 'ConfigLeverageTime' in i.keys():
                                    editplan.ConfigLeverageTime = i['ConfigLeverageTime']
                                if 'CommentsLeverage' in i.keys():
                                    editplan.CommentsLeverage = i['CommentsLeverage']
                                if 'ConfigSmartItem' in i.keys():
                                    editplan.ConfigSmartItem = i['ConfigSmartItem']
                                if 'ConfigSmartItemPer' in i.keys():
                                    editplan.ConfigSmartItemPer = i['ConfigSmartItemPer']
                                if 'ConfigSmartTime' in i.keys():
                                    editplan.ConfigSmartTime = i['ConfigSmartTime']
                                if 'CommentsSmart' in i.keys():
                                    editplan.CommentsSmart = i['CommentsSmart']
                                if 'ProjectTestSKUOptimize' in i.keys():
                                    editplan.ProjectTestSKUOptimize = i['ProjectTestSKUOptimize']
                                if 'AttendTimeOptimize' in i.keys():
                                    editplan.AttendTimeOptimize = i['AttendTimeOptimize']
                                if 'SKU1' in i.keys():
                                    editplan.SKU1 = i['SKU1']
                                if 'SKU2' in i.keys():
                                    editplan.SKU2 = i['SKU2']
                                if 'SKU3' in i.keys():
                                    editplan.SKU3 = i['SKU3']
                                if 'SKU4' in i.keys():
                                    editplan.SKU4 = i['SKU4']
                                if 'SKU5' in i.keys():
                                    editplan.SKU5 = i['SKU5']
                                if 'SKU6' in i.keys():
                                    editplan.SKU6 = i['SKU6']
                                if 'SKU7' in i.keys():
                                    editplan.SKU7 = i['SKU7']
                                if 'SKU8' in i.keys():
                                    editplan.SKU8 = i['SKU8']
                                if 'SKU9' in i.keys():
                                    editplan.SKU9 = i['SKU9']
                                if 'SKU10' in i.keys():
                                    editplan.SKU10 = i['SKU10']
                                if 'SKU11' in i.keys():
                                    editplan.SKU11 = i['SKU11']
                                if 'SKU12' in i.keys():
                                    editplan.SKU12 = i['SKU12']
                                if 'SKU13' in i.keys():
                                    editplan.SKU13 = i['SKU13']
                                if 'SKU14' in i.keys():
                                    editplan.SKU14 = i['SKU14']
                                if 'SKU15' in i.keys():
                                    editplan.SKU15 = i['SKU15']
                                if 'SKU16' in i.keys():
                                    editplan.SKU16 = i['SKU16']
                                if 'SKU17' in i.keys():
                                    editplan.SKU17 = i['SKU17']
                                if 'SKU18' in i.keys():
                                    editplan.SKU18 = i['SKU18']
                                if 'SKU19' in i.keys():
                                    editplan.SKU19 = i['SKU19']
                                if 'SKU20' in i.keys():
                                    editplan.SKU20 = i['SKU20']
                                if 'ConfigRetestCycle' in i.keys():
                                    editplan.ConfigRetestCycle = i['ConfigRetestCycle']
                                if 'ConfigRetestSKU' in i.keys():
                                    editplan.ConfigRetestSKU = i['ConfigRetestSKU']
                                if 'ConfigRetestTime' in i.keys():
                                    editplan.ConfigRetestTime = i['ConfigRetestTime']
                                editplan.editor = request.session.get('user_name')
                                editplan.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                editplan.save()
                            #create
                            else:
                                # print('create')
                                updatedic={}
                                for j in i.keys():
                                    updatedic[j]=i[j]
                                updatedic['Project']=responseData['project']
                                updatedic['Projectinfo']=TestProjectSW.objects.get(**dic_Project)
                                updatedic['editor']=request.session.get('user_name')
                                updatedic['edit_time']= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                # print(updatedic)
                                # for m in updatedic:
                                #     print (m,type(updatedic[m]))
                                RetestItemSW.objects.create(**updatedic)
                        else:
                            print("Case_ID&Case_Name&Test_Items can't be null")
                    #Others
                    else:
                        # print ('others')
                        if 'TestItems' in i.keys():
                            check_dic = {'Customer':responseData['customer'],'Phase':Phase,'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d'],'TestItems':i['TestItems']}
                        else:
                            check_dic = {'Customer':responseData['customer'],'Phase':Phase,'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d']}
                        # check_dic = {'Customer':i['Customer'],'Phase':i['Phase'],'ItemNo_d': i['Case_ID'], 'Item_d': i['Case_Name'],'TestItems':i['Test_Items']}
                        # print(check_dic)
                        check_list = TestItemSW.objects.filter(**check_dic).first()
                        itemsinfo = TestItemSW.objects.get(id=check_list.id)
                        if itemsinfo:
                            # print(itemsinfo)
                            editplan=TestPlanSW.objects.filter(Items=itemsinfo,Projectinfo=Projectinfos).first()
                            # print(type(editplan))

                            if editplan:
                                # print(editplan)
                                if 'FeatureSupport' in i.keys():
                                    editplan.FeatureSupport=i['FeatureSupport']
                                if 'BaseTimeSupport' in i.keys():
                                    editplan.BaseTimeSupport = i['BaseTimeSupport']
                                if 'TE' in i.keys():
                                    editplan.TE = i['TE']
                                if 'Schedule' in i.keys():
                                    editplan.Schedule = i['Schedule']
                                if 'ProjectTestSKUfollowMatrix' in i.keys():
                                    editplan.ProjectTestSKUfollowMatrix = i['ProjectTestSKUfollowMatrix']
                                if 'TimewConfigFollowmatrix' in i.keys():
                                    editplan.TimewConfigFollowmatrix = i['TimewConfigFollowmatrix']
                                if 'ConfigAutomationItem' in i.keys():
                                    editplan.ConfigAutomationItem = i['ConfigAutomationItem']
                                if 'ConfigAutomationTime' in i.keys():
                                    editplan.ConfigAutomationTime = i['ConfigAutomationTime']
                                if 'ConfigLeverageItem' in i.keys():
                                    editplan.ConfigLeverageItem = i['ConfigLeverageItem']
                                if 'ConfigLeverageTime' in i.keys():
                                    editplan.ConfigLeverageTime = i['ConfigLeverageTime']
                                if 'CommentsLeverage' in i.keys():
                                    editplan.CommentsLeverage = i['CommentsLeverage']
                                if 'ConfigSmartItem' in i.keys():
                                    editplan.ConfigSmartItem = i['ConfigSmartItem']
                                if 'ConfigSmartItemPer' in i.keys():
                                    editplan.ConfigSmartItemPer = i['ConfigSmartItemPer']
                                if 'ConfigSmartTime' in i.keys():
                                    editplan.ConfigSmartTime = i['ConfigSmartTime']
                                if 'CommentsSmart' in i.keys():
                                    editplan.CommentsSmart = i['CommentsSmart']
                                if 'ProjectTestSKUOptimize' in i.keys():
                                    editplan.ProjectTestSKUOptimize = i['ProjectTestSKUOptimize']
                                if 'AttendTimeOptimize' in i.keys():
                                    editplan.AttendTimeOptimize = i['AttendTimeOptimize']
                                if 'SKU1' in i.keys():
                                    editplan.SKU1 = i['SKU1']
                                if 'SKU2' in i.keys():
                                    editplan.SKU2 = i['SKU2']
                                if 'SKU3' in i.keys():
                                    editplan.SKU3 = i['SKU3']
                                if 'SKU4' in i.keys():
                                    editplan.SKU4 = i['SKU4']
                                if 'SKU5' in i.keys():
                                    editplan.SKU5 = i['SKU5']
                                if 'SKU6' in i.keys():
                                    editplan.SKU6 = i['SKU6']
                                if 'SKU7' in i.keys():
                                    editplan.SKU7 = i['SKU7']
                                if 'SKU8' in i.keys():
                                    editplan.SKU8 = i['SKU8']
                                if 'SKU9' in i.keys():
                                    editplan.SKU9 = i['SKU9']
                                if 'SKU10' in i.keys():
                                    editplan.SKU10 = i['SKU10']
                                if 'SKU11' in i.keys():
                                    editplan.SKU11 = i['SKU11']
                                if 'SKU12' in i.keys():
                                    editplan.SKU12 = i['SKU12']
                                if 'SKU13' in i.keys():
                                    editplan.SKU13 = i['SKU13']
                                if 'SKU14' in i.keys():
                                    editplan.SKU14 = i['SKU14']
                                if 'SKU15' in i.keys():
                                    editplan.SKU15 = i['SKU15']
                                if 'SKU16' in i.keys():
                                    editplan.SKU16 = i['SKU16']
                                if 'SKU17' in i.keys():
                                    editplan.SKU17 = i['SKU17']
                                if 'SKU18' in i.keys():
                                    editplan.SKU18 = i['SKU18']
                                if 'SKU19' in i.keys():
                                    editplan.SKU19 = i['SKU19']
                                if 'SKU20' in i.keys():
                                    editplan.SKU20 = i['SKU20']
                                if 'ConfigRetestCycle' in i.keys():
                                    editplan.ConfigRetestCycle = i['ConfigRetestCycle']
                                if 'ConfigRetestSKU' in i.keys():
                                    editplan.ConfigRetestSKU = i['ConfigRetestSKU']
                                if 'ConfigRetestTime' in i.keys():
                                    editplan.ConfigRetestTime = i['ConfigRetestTime']
                                editplan.editor = request.session.get('user_name')
                                editplan.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                editplan.save()
                        else:
                            if 'TestItems' in i.keys():
                                item_nodata.append({'Customer': responseData['customer'], 'Phase': Phase, 'ItemNo_d': i['ItemNo_d'],
                                             'Item_d': i['Item_d'], 'TestItems': i['TestItems']})
                            else:
                                item_nodata.append({'Customer': responseData['customer'], 'Phase': Phase, 'ItemNo_d': i['ItemNo_d'],
                                             'Item_d': i['Item_d']})
                            #need update testitem first

            # print(type(Phase))
            if responseData['phase'] == 0:
                Phase = 'B(FVT)'
            if responseData['phase'] == 1:
                Phase = 'C(SIT)'
            if responseData['phase'] == 2:
                Phase = 'FFRT'
            if responseData['phase'] == 3:
                Phase = 'Others'

            dic_Project_search = {'Customer': responseData['customer'],
                               'Project': responseData['project'], 'Phase': Phase}
            # print(dic_Project)
            Projectinfos_search = TestProjectSW.objects.filter(**dic_Project_search).first()
            # print(Projectinfos.Owner.all())
            # print(Projectinfos)
            canEdit = 0
            current_user = request.session.get('user_name')
            if Projectinfos_search:
                for k in Projectinfos_search.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if k.username == current_user:
                        canEdit = 1
                        break
                SKUlist = [Projectinfos_search.SKU1, Projectinfos_search.SKU2, Projectinfos_search.SKU3, Projectinfos_search.SKU4,
                           Projectinfos_search.SKU5,
                           Projectinfos_search.SKU6, Projectinfos_search.SKU7, Projectinfos_search.SKU8, Projectinfos_search.SKU9,
                           Projectinfos_search.SKU10,
                           Projectinfos_search.SKU11, Projectinfos_search.SKU12, Projectinfos_search.SKU13, Projectinfos_search.SKU14,
                           Projectinfos_search.SKU15,
                           Projectinfos_search.SKU16, Projectinfos_search.SKU17, Projectinfos_search.SKU18, Projectinfos_search.SKU19,
                           Projectinfos_search.SKU20]
                n = 1
                for l in SKUlist:
                    if l:
                        # print(l)
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": l.split('/')[1], "CPU": l.split('/')[0]})
                        n += 1
            # print(SKU)
            if canEdit:
                itemlist = []
                for i in TestItemSW.objects.filter(Customer=responseData['customer'], Phase=Phase):
                    itemlist.append(i.id)
                # print (itemlist,'yyy')
                existitem = []
                for i in Projectinfos.testplansw_set.all():
                    existitem.append(i.Items.id)
                # print(existitem)
                for i in itemlist:
                    if i in existitem:
                        continue
                    else:
                        # print(TestProjectSW.objects.filter(**dic_Project).first())
                        TestPlanSW.objects.create(Items=TestItemSW.objects.get(id=i),
                                                  Projectinfo=TestProjectSW.objects.filter(**dic_Project).first())
                # print (TestItemSW.objects.all().values('Category2').distinct().count())
            m = 0
            for i in TestItemSW.objects.all().values('Category2').distinct():
                # print(type(i),i)
                title.append({"caseid": i['Category2'], 'hasChildren': 'true'})
                m += 1
            dic_Project = {'Customer': responseData['customer'], 'Project': responseData['project'], 'Phase': Phase}
            if RetestItemSW.objects.filter(**dic_Project).first():
                title.append({"caseid":  "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution’s issue ) for full function test"})
            # print(title)

            updateData = {
                "MockData": title,
                "SKU": SKU,
                "selectMsg": combine,
                "canEdit": canEdit
            }
        #update
        if 'Edit' in responseData.keys():
            Editdata = json.loads(responseData['Edit'])
        return HttpResponse(json.dumps(updateData), content_type="application/json")
    return render(request, 'TestPlanSW/TestPlanSW_edit20200118.html', locals())
#TestPlan_ME search
def TestPlanSW_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Search"
    # print(Skin)
    newContents = [
        # {"id": 20191264, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
        #  "conAitem": 0, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 0, "CST": 80,"starttime":102,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191265, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 0, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 0, "CST": 80,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191266, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
        #  "conAitem": 1, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 1, "CST": 80,"starttime":102,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191267, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #   "conAitem": 0,"BTS":10,"FS":0,"TE":'WILL',"schedule":'2020/1/2',"CAT":100,"conLitem":1,"CLT":100,"conSitem":0,"CST":80,
        #  "TFC":80,"comments1":"备注1","comments2":"备注2","proTS":55,"ATO":99,"CRC":12,"CRS":15,"CRT":19,"conSitemInAll":1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191268, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #   "conAitem": 0,"BTS":10,"FS":0,"TE":'WILL',"schedule":'2020/1/2',"CAT":100,"conLitem":1,"CLT":100,"conSitem":0,"CST":80,
        #  "TFC":80,"comments1":"备注1","comments2":"备注2","proTS":55,"ATO":99,"CRC":12,"CRS":15,"CRT":19,"conSitemInAll":1,
        #  "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191269, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 0, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 0, "CST": 80,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
    ]

    title = [
        # {"caseid": "Basic", 'hasChildren': 'true',"unattendedtime": 6950, "basetimeA": 0,"basetime": 6950,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Interaction", 'hasChildren': 'true',"unattendedtime": 6950, "basetimeA": 0,"basetime": 6950,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Connectivity", 'hasChildren': 'true',"unattendedtime": 6950, "basetimeA": 0,"basetime": 6950,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Process and Stroage", 'hasChildren': 'true',"unattendedtime": 6952, "basetimeA": 0,"basetime": 6952,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Performance", 'hasChildren': 'true',"unattendedtime": 6925, "basetimeA": 0,"basetime": 6925,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Game Test", 'hasChildren': 'true',"unattendedtime": 6395, "basetimeA": 0,"basetime": 6935,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Stress", 'hasChildren': 'true',"unattendedtime": 6395, "basetimeA": 0,"basetime": 6495,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Application", 'hasChildren': 'true',"unattendedtime": 6595, "basetimeA": 0,"basetime": 6695,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Compal internal", 'hasChildren': 'true',"unattendedtime": 6975, "basetimeA": 0,"basetime": 6695,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Game unique", 'hasChildren': 'true',"unattendedtime": 6957, "basetimeA": 0,"basetime": 6957,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Linux and DOS", 'hasChildren': 'true',"unattendedtime": 6795, "basetimeA": 0,"basetime": 6695,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Accessories", 'hasChildren': 'true',"unattendedtime": 6795, "basetimeA": 0,"basetime": 6975,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Gaming Unique", 'hasChildren': 'true',"unattendedtime": 6795, "basetimeA": 0,"basetime": 6795,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
    ]
    SKU = [
        # {"skuNo": "SKU1", "VGA": "UMA", "CPU": "i3-8145U"},
        # {"skuNo": "SKU2", "VGA": "N17S-G2-A1", "CPU": "i5-8265U"},
        # {"skuNo": "SKU2", "VGA": "UMA", "CPU": "i5-8265U"},
        # {"skuNo": "SKU3", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"},
        # {"skuNo": "SKU4", "VGA": "Picasso", "CPU": "i7-8565U"}, {"skuNo": "SKU5", "VGA": "UMA", "CPU": "i7-8565U"},
        # {"skuNo": "SKU6", "VGA": "N17S-G2-A1", "CPU": "i7-8565U"},
        # {"skuNo": "SKU7", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"}
    ]
    combine = {
        # "C38(NB)": [{"project": "ELMV2", "phase": [0, 1, 2, 3]}, {"project": "FLY00", "phase": [2, 3]},
        #             {"project": "ELZP5", "phase": [1]}, {"project": "ELZP7", "phase": [1, 2, 3]}],
        # "C38(AIO)": [{"project": "FLMS0", "phase": [1, 2, 3]}, {"project": "FLMS1", "phase": [1, 2, 3]},
        #              {"project": "FLMS2", "phase": [1, 2, 3]}],
        # "A39": [{"project": "DLAE1", "phase": [1, 2, 3]}, {"project": "DLAE2", "phase": [1, 2, 3]},
        #         {"project": "DLAE3", "phase": [1, 2, 3]}],
        # "Other": [{"project": "OTHER", "phase": [1, 2, 3]}]
    }
    Customer_list = TestProjectSW.objects.all().values('Customer').distinct().order_by('Customer')

    for i in Customer_list:
        Customerlist = []
        for j in TestProjectSW.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            phaselist = []
            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            for m in TestProjectSW.objects.filter(**dic).values('Phase').distinct().order_by('Phase'):

                if m['Phase'] == "B(FVT)":
                    PhaseValue = 0
                if m['Phase'] == "C(SIT)":
                    PhaseValue = 1
                if m['Phase'] == "FFRT":
                    PhaseValue = 2
                if m['Phase'] == "Others":
                    PhaseValue = 3
                phaselist.append(PhaseValue)
            Projectinfo['phase'] = phaselist
            Projectinfo['project'] = j['Project']
            Customerlist.append(Projectinfo)
        combine[i['Customer']] = Customerlist
    # print (request.method)
    print(request.GET,request.GET.get("action"),request.POST)
    # print(request.body)
    if request.method == "GET":
        if request.GET.get("action") == "first":
            return HttpResponse(json.dumps(combine), content_type="application/json")
        elif request.GET.get("action") == "search":
            # if request.GET.get("customer") == "C38(NB)":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            # print(type(Phase))
            if Phase == '0':
                Phase = 'B(FVT)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'FFRT'
            if Phase == '3':
                Phase = 'Others'
            dic_Item = {'Customer': Customer, 'Phase': Phase}
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
            # print(Projectinfos.Owner.all())
            # print(Projectinfos)
            canEdit = 0
            current_user = request.session.get('user_name')
            if Projectinfos:
                SKUlist = [Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                           Projectinfos.SKU5,
                           Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                           Projectinfos.SKU10,
                           Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                           Projectinfos.SKU15,
                           Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                           Projectinfos.SKU20]
                n = 1
                for i in SKUlist:
                    if i:
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
                        n += 1
            # print(SKU)
            m = 0
            for i in TestItemSW.objects.filter(**dic_Item).values('Category2').distinct():
                # print(type(i),i)
                title.append({"caseid": i['Category2'], 'hasChildren': 'true'})
                m += 1
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            if RetestItemSW.objects.filter(**dic_Project).first():
                title.append({
                                 "caseid": "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution’s issue ) for full function test",
                                 'hasChildren': 'true'})
            # print(title)

            updateData = {
                "MockData": title,
                "SKU": SKU,
                "selectMsg": combine,
                # "canEdit": canEdit
            }
            return HttpResponse(json.dumps(updateData), content_type="application/json")
        elif request.GET.get("action") == "getContent":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            Category2 = request.GET.get('contents')
            # print(Category2)
            # print(type(Phase))
            if Phase == '0':
                Phase = 'B(FVT)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'FFRT'
            if Phase == '3':
                Phase = 'Others'
            dicItem = {'Customer': Customer, 'Phase': Phase, 'Category2': Category2}
            # print(dicItem)
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            if request.GET.get(
                    "contents") == "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution’s issue ) for full function test":
                RetestItemSWinfo = RetestItemSW.objects.filter(**dic_Project)
                # print('Retest')
                if RetestItemSWinfo:
                    for i in RetestItemSWinfo:
                        planOptimize = []
                        SKUlist = [i.SKU1, i.SKU2, i.SKU3, i.SKU4, i.SKU5,
                                   i.SKU6, i.SKU7, i.SKU8, i.SKU9, i.SKU10,
                                   i.SKU11, i.SKU12, i.SKU13, i.SKU14, i.SKU15,
                                   i.SKU16, i.SKU17, i.SKU18, i.SKU19, i.SKU20]

                        for j in SKUlist:
                            if j:
                                planOptimize.append(j)
                            # print(planOptimize)
                        newContents.append(
                            {  # Reitem
                                "id": i.id, "caseid": i.ItemNo_d, "casename": i.Item_d,
                                "testitem": i.TestItems,
                                "version": i.Version,
                                "releasedate": i.ReleaseDate, "owner": i.Owner,
                                "priority": i.Priority,
                                # TDMSTotalTime前端直接后两项加总
                                "basetime": i.BaseTime,
                                "unattendedtime": i.TDMSUnattendedTime,
                                "basetimeA": i.BaseAotomationTime1SKU,
                                "chramshell": i.Chramshell, "conver_NB": i.ConvertibaleNBMode,
                                "conver_Yoga": i.ConvertibaleYogaPadMode,
                                "detach_Pad": i.DetachablePadMode, "detach_W": i.DetachableWDockmode,
                                "PhaseF": i.PhaseFVT, "PhaseS": i.PhaseSIT, 'PhaseFFRT': i.PhaseFFRT,
                                "coverage": i.Coverage,
                                'FS': i.FeatureSupport, 'TE': i.TE, 'schedule': i.Schedule,
                                'starttime': i.ProjectTestSKUfollowMatrix, 'conAitem': i.ConfigAutomationItem,
                                'conLitem': i.ConfigLeverageItem, 'comments1': i.CommentsLeverage,
                                'conSitem': i.ConfigSmartItem,
                                'comments2': i.CommentsSmart, "planOptimize": planOptimize, 'CRC': i.ConfigRetestCycle,
                                'CRS': i.ConfigRetestSKU, 'CRT': i.ConfigRetestTime,
                                # no need edit
                                'BTS': i.BaseTimeSupport, 'TFC': i.TimewConfigFollowmatrix,
                                'conAtime': i.ConfigAutomationTime, 'conLtime': i.ConfigLeverageTime,
                                'conSitemInAll': i.ConfigSmartItem, 'conStime': i.ConfigSmartTime,
                                'proTS': i.ProjectTestSKUOptimize, 'ATO': i.AttendTimeOptimize
                            })
                    # print(newContents)
            else:
                # print('Others')
                Iteminfos = TestItemSW.objects.filter(**dicItem)
                Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
                # print(Projectinfos.Owner.all())
                # print(Iteminfos)
                # print(Projectinfos)
                if Projectinfos:
                    x = 0
                    for h in Iteminfos:
                        for i in TestPlanSW.objects.filter(Items=h, Projectinfo=Projectinfos):
                            x += 1
                            # print(i,type(i))
                            # print(i.id)
                            planOptimize = []
                            SKUlist = [i.SKU1, i.SKU2, i.SKU3, i.SKU4, i.SKU5,
                                       i.SKU6, i.SKU7, i.SKU8, i.SKU9, i.SKU10,
                                       i.SKU11, i.SKU12, i.SKU13, i.SKU14, i.SKU15,
                                       i.SKU16, i.SKU17, i.SKU18, i.SKU19, i.SKU20]

                            for j in SKUlist:
                                if j:
                                    planOptimize.append(j)
                                # print(planOptimize)
                            # print(i.ConfigSmartItemPer,i.ConfigSmartTime)
                            newContents.append(
                                {  # item
                                    "id": i.id, "caseid": i.Items.ItemNo_d, "casename": i.Items.Item_d,
                                    "testitem": i.Items.TestItems,
                                    "version": i.Items.Version,
                                    "releasedate": i.Items.ReleaseDate, "owner": i.Items.Owner,
                                    "priority": i.Items.Priority,
                                    # TDMSTotalTime前端直接后两项加总
                                    "basetime": i.Items.BaseTime,
                                    "unattendedtime": i.Items.TDMSUnattendedTime,
                                    "basetimeA": i.Items.BaseAotomationTime1SKU,
                                    "chramshell": i.Items.Chramshell, "conver_NB": i.Items.ConvertibaleNBMode,
                                    "conver_Yoga": i.Items.ConvertibaleYogaPadMode,
                                    "detach_Pad": i.Items.DetachablePadMode, "detach_W": i.Items.DetachableWDockmode,
                                    "PhaseF": i.Items.PhaseFVT, "PhaseS": i.Items.PhaseSIT,
                                    'PhaseFFRT': i.Items.PhaseFFRT,
                                    "coverage": i.Items.Coverage,
                                    # plan
                                    'FS': i.FeatureSupport, 'TE': i.TE, 'schedule': i.Schedule,
                                    'starttime': i.ProjectTestSKUfollowMatrix, 'conAitem': i.ConfigAutomationItem,
                                    'conLitem': i.ConfigLeverageItem, 'comments1': i.CommentsLeverage,
                                    'conSitem': i.ConfigSmartItem,
                                    'comments2': i.CommentsSmart, "planOptimize": planOptimize,
                                    'CRC': i.ConfigRetestCycle, 'CRS': i.ConfigRetestSKU, 'CRT': i.ConfigRetestTime,
                                    # no need edit
                                    'BTS': i.BaseTimeSupport, 'TFC': i.TimewConfigFollowmatrix,
                                    'CAT': i.ConfigAutomationTime, 'CLT': i.ConfigLeverageTime,
                                    'conSitemInAll': i.ConfigSmartItemPer, 'CST': i.ConfigSmartTime,
                                    'proTS': i.ProjectTestSKUOptimize, 'ATO': i.AttendTimeOptimize
                                })
                    # print(newContents)
                    # print(x)
            # print(newContents)
            return HttpResponse(json.dumps(newContents), content_type="application/json")

    return render(request, 'TestPlanSW/TestPlanSW_search.html', locals())

def ItemSW_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "TestPlan/SW/Itemload"

    SWItem_lists = [{'Customer':'Customer','Phase':'Phase','ItemNo_d': 'ItemNo', 'Item_d': 'Item','TestItems':'TestItems'}]

    message_err = 0
    # print(request.POST,request.method)
    if request.method == "POST":
        # print(request.POST)
        if 'type' in request.POST:
            err_ok = 0
            xlsxlist = request.POST.get('upload')
            # print (simplejson.loads(xlsxlist))
            n=0
            j=0
            k=0

            for i in simplejson.loads(xlsxlist):
                n+=1
                SWItem_dic = {}
                # print(i)
                # print (i['Customer'])
                if 'TestItems' in i.keys():
                    check_dic = {'Customer':i['Customer'],'Phase':i['Phase'],'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d'],'TestItems':i['TestItems']}
                else:
                    check_dic = {'Customer':i['Customer'],'Phase':i['Phase'],'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d']}
                # check_dic = {'Customer':i['Customer'],'Phase':i['Phase'],'ItemNo_d': i['Case_ID'], 'Item_d': i['Case_Name'],'TestItems':i['Test_Items']}
                # print(check_dic)
                check_list = TestItemSW.objects.filter(**check_dic).first()
                # print (check_list)
                if check_list:
                    # print (check_list)
                    j+=1
                    # err_ok = 1
                    SWItem_dic['Customer']=i['Customer']
                    SWItem_dic['Phase'] = i['Phase']
                    SWItem_dic['ItemNo_d'] = i['ItemNo_d']
                    SWItem_dic['Item_d'] = i['Item_d']
                    if 'TestItems' in i.keys():
                        SWItem_dic['TestItems'] = i['TestItems']
                    SWItem_lists.append(SWItem_dic)
                    # print(SWItem_dic)
                    Itemmodel = TestItemSW.objects.get(id=check_list.id)
                    # print(Itemmodel,type(Itemmodel))
                    if 'Customer' in i.keys():
                        Itemmodel.Customer = i['Customer']
                    if 'Phase' in i.keys():
                        Itemmodel.Phase = i['Phase']
                    if 'ItemNo_d' in i.keys():
                        Itemmodel.ItemNo_d = i['ItemNo_d']
                    if 'Item_d' in i.keys():
                        Itemmodel.Item_d = i['Item_d']
                    if 'TestItems' in i.keys():
                        Itemmodel.TestItems = i['TestItems']
                    if 'Category' in i.keys():
                        Itemmodel.Category = i['Category']
                    if 'Category2' in i.keys():
                        Itemmodel.Category2 = i['Category2']
                    if 'Version' in i.keys():
                        Itemmodel.Version = i['Version']
                    if 'ReleaseDate' in i.keys():
                        # print(i['Release_date'])
                        Itemmodel.ReleaseDate = i['ReleaseDate']
                    if 'Owner' in i.keys():
                        Itemmodel.Owner = i['Owner']
                    if 'Priority' in i.keys():
                        Itemmodel.Priority = i['Priority']
                    if 'TDMSTotalTime' in i.keys():
                        Itemmodel.TDMSTotalTime = i['TDMSTotalTime']
                    if 'BaseTime' in i.keys():
                        # print(i['Base_time'])
                        Itemmodel.BaseTime = i['BaseTime']
                    if 'TDMSUnattendedTime' in i.keys():
                        Itemmodel.TDMSUnattendedTime = i['TDMSUnattendedTime']
                    if 'BaseAotomationTime1SKU' in i.keys():
                        Itemmodel.BaseAotomationTime1SKU = i['BaseAotomationTime1SKU']
                    if 'Chramshell' in i.keys():
                        Itemmodel.Chramshell = i['Chramshell']
                    if 'ConvertibaleNBMode' in i.keys():
                        Itemmodel.ConvertibaleNBMode = i['ConvertibaleNBMode']
                    if 'ConvertibaleYogaPadMode' in i.keys():
                        Itemmodel.ConvertibaleYogaPadMode = i['ConvertibaleYogaPadMode']
                    if 'DetachablePadMode' in i.keys():
                        Itemmodel.DetachablePadMode = i['DetachablePadMode']
                    if 'DetachableWDockmode' in i.keys():
                        Itemmodel.DetachableWDockmode = i['DetachableWDockmode']
                    if 'PhaseFVT' in i.keys():
                        Itemmodel.PhaseFVT = i['PhaseFVT']
                        # print(i['FVT'])
                        # print(Itemmodel.PhaseFVT)
                    if 'PhaseSIT' in i.keys():
                        Itemmodel.PhaseSIT = i['PhaseSIT']
                    if 'PhaseFFRT' in i.keys():
                        Itemmodel.PhaseFFRT = i['PhaseFFRT']
                    if 'Coverage' in i.keys():
                        Itemmodel.Coverage = i['Coverage']
                    Itemmodel.save()
                    continue
                else:
                    # print('save')
                    # print(i)
                    k+=1
                    Itemmodel = TestItemSW()
                    if 'Customer' in i.keys():
                        Itemmodel.Customer = i['Customer']
                    if 'Phase' in i.keys():
                        Itemmodel.Phase = i['Phase']
                    if 'ItemNo_d' in i.keys():
                        Itemmodel.ItemNo_d = i['ItemNo_d']
                    if 'Item_d' in i.keys():
                        Itemmodel.Item_d = i['Item_d']
                    if 'TestItems' in i.keys():
                        Itemmodel.TestItems = i['TestItems']
                    if 'Category' in i.keys():
                        Itemmodel.Category = i['Category']
                    if 'Category2' in i.keys():
                        Itemmodel.Category2 = i['Category2']
                    if 'Version' in i.keys():
                        Itemmodel.Version = i['Version']
                    if 'ReleaseDate' in i.keys():
                        Itemmodel.ReleaseDate = i['ReleaseDate']
                    if 'Owner' in i.keys():
                        Itemmodel.Owner = i['Owner']
                    if 'Priority' in i.keys():
                        Itemmodel.Priority = i['Priority']
                    if 'TDMSTotalTime' in i.keys():
                        Itemmodel.TDMSTotalTime = i['TDMSTotalTime']
                    if 'BaseTime' in i.keys():
                        Itemmodel.BaseTime = i['BaseTime']
                    if 'TDMSUnattendedTime' in i.keys():
                        Itemmodel.TDMSUnattendedTime = i['TDMSUnattendedTime']
                    if 'BaseAotomationTime1SKU' in i.keys():
                        Itemmodel.BaseAotomationTime1SKU = i['BaseAotomationTime1SKU']
                    if 'Chramshell' in i.keys():
                        Itemmodel.Chramshell = i['Chramshell']
                    if 'ConvertibaleNBMode' in i.keys():
                        Itemmodel.ConvertibaleNBMode = i['ConvertibaleNBMode']
                    if 'ConvertibaleYogaPadMode' in i.keys():
                        Itemmodel.ConvertibaleYogaPadMode = i['ConvertibaleYogaPadMode']
                    if 'DetachablePadMode' in i.keys():
                        Itemmodel.DetachablePadMode = i['DetachablePadMode']
                    if 'DetachableWDockmode' in i.keys():
                        Itemmodel.DetachableWDockmode = i['DetachableWDockmode']
                    if 'PhaseFVT' in i.keys():
                        Itemmodel.PhaseFVT = i['PhaseFVT']
                    if 'PhaseSIT' in i.keys():
                        Itemmodel.PhaseSIT = i['PhaseSIT']
                    if 'PhaseFFRT' in i.keys():
                        Itemmodel.PhaseFFRT = i['PhaseFFRT']
                    if 'Coverage' in i.keys():
                        Itemmodel.Coverage = i['Coverage']
                    Itemmodel.save()
                    # print('ttt')
            # if not message_CDM:
            #     message_CDM = "Upload Successfully"
            # print(message_CDM)
            print(n,j,k)
            datajason={
                'err_ok':err_ok,
                'content': SWItem_lists
            }
            # print(datajason)
            # print(json.dumps(datajason))
            return HttpResponse(json.dumps(datajason), content_type="application/json")

    return render(request, 'TestPlanSW/itemuploadSW.html', locals())