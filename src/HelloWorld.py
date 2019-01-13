# -*- encoding: utf8 -*-
import requests
import time
import sys
import re as regx
import MetaInfos as meta
from pygame import mixer
from bs4 import BeautifulSoup as bs

######################################################################
#########################    SETTINGS    #############################
######################################################################

check_time_term = 2        #3초에 한번 확인
id = "id"           #아이디 입력
pw = "pw"            #패스워드 입력
reserve_date = '20190113'   #예약 날짜 입력"
time_min = '1950'           #예약 희망 시간 최저
time_max = '2053'           #예약 희망 시간 최대
depart_station = '동대구'
arrive_station = '수서'


########################    STAION LIST    ###########################
'공주', '광주송정', '김천구미', '나주', '대전', '동대구', '동탄', '목포', '부산', '수서', '신경주', '오송', '울산', '익산', '정읍', '지제', '천안아산'
######################################################################



######################################################################
######################    REQUEST META INFO     ######################
######################################################################



######################################################################
##########################    LOGICS    ##############################
######################################################################

def login(id, pw):
    header = dict(meta.common_header)
    header["Referer"] = meta.login_referer
    header['Content-Type'] = 'application/x-www-form-urlencoded'

    # 더 확실한 키워드를 찾아보자.
    login_success_keyword = 'location.replace(\'/main.do\')'

    response = requests.post(meta.login_request_url,
                             headers=header,
                             params=login_param(id, pw))

    if response.cookies and response.cookies['JSESSIONID_ETK']:
        print ("get cookie from login response:"+response.cookies['JSESSIONID_ETK'])
        meta.my_cookie["JSESSIONID_ETK"] = response.cookies['JSESSIONID_ETK']

    if response.status_code != 200:
        return False
    elif ('오류' in response.text) or ('실패' in response.text) or ('존재' in response.text):
        return False
    elif login_success_keyword in response.text:
        return True


def login_param(id, pw):
    return {
        'rsvTpCd': None,
        'goUrl': None,
        'from': None,
        'srchDvCd': '1',
        'srchDvNm': id,
        'hmpgPwdCphd': pw
    }


def reserve(reserv_targets):
    header = dict(meta.common_header)
    header['Cookie'] = "SR_MB_CD_NO="+str(id) +"; JSESSIONID_ETK="+meta.my_cookie['JSESSIONID_ETK']
    header['Referer'] = meta.check_seat_url

    for tr in reserv_targets:
        response = requests.post(meta.reservation_url,
                                 headers=header,
                                 params=reservation_param(tr))

        if not (response.status_code == 200 and "location.replace('/hpg/hra/02/requestReservationInfo.do?pageId=TK0101030000')" in response.text) :
            continue

        response = requests.get(meta.reservation_url2, headers = header)
        if not (response.status_code == 200 and "location.replace('confirmReservationInfo.do?pageId=TK0101030000')" in response.text):
            continue

        response = requests.get(meta.reservation_confirm_url, headers = header)
        if not (response.status_code == 200 and "10분 내에 결제하지 않으면 예약이 취소됩니다" in response.text):
            continue

        printPretty("예약 성공")
        reserve_id = bs(response.text,'html.parser').find('input', attrs={"name":"pnrNo"})
        print(reserve_id)

        return reserve_id
        #예약 성공하면 반환값 리턴하면서 종료
    return False


def reservation_param(tr):
    param = dict(meta.reserve_param)

    train_info_list = bs(str(tr), 'html.parser').select("td.trnNo > input")
    train_info_dict = { bs(str(info), 'html.parser').find()['name'].split('[')[0]: bs(str(info),'html.parser').find()['value'] for info in train_info_list }

    param['dptDt1'] = train_info_dict['dptDt']
    param['runDt1'] = train_info_dict['runDt']
    param['arvStnConsOrdr1'] = train_info_dict['arvStnConsOrdr']
    param['arvStnRunOrdr1'] = train_info_dict['arvStnRunOrdr']
    param['arvRsStnCd1'] = train_info_dict['arvRsStnCd']
    param['dirSeatAttCd1'] = '000'
    param['dptRsStnCd1'] = train_info_dict['dptRsStnCd']
    param['dptStnConsOrdr1'] = train_info_dict['dptStnConsOrdr']
    param['dptTm1'] = train_info_dict['dptTm']
    param['jrnySqno1'] = train_info_dict['jrnySqno']
    param['locSeatAttCd1'] = "000"
    param['reqTime'] = int(time.time()*1000) #현재시간
    param['rqSeatAttCd1'] = train_info_dict['seatAttCd']
    param['stlbTrnClsfCd1'] = train_info_dict['stlbTrnClsfCd']
    param['trnGpCd1'] = train_info_dict['trnGpCd']
    param['trnNo1'] = train_info_dict['trnNo']
    param['trnOrdrNo1'] = train_info_dict['trnOrdrNo'] #화면에서 몇번째 라인에 있던 열차인지

    return param


#빈 좌석이 있는지 확인
def find_empty_seats(start, dest, date, time_min ='000000', time_max ='220000'):
    header = dict(meta.common_header)
    header["Referer"] = "https://etk.srail.co.kr/main.do"
    header['Content-Type'] = 'application/x-www-form-urlencoded'

    print("좌석 정보를 조회합니다..")
    response = requests.post(meta.check_seat_url,
                             headers=header,
                             params=finding_seats_param(start, dest, date))

    #열차 정보
    trains = bs(response.text, 'html.parser').select("tbody > tr")

    #매진이라도 열차가 하나라도 없다면 종료되도록
    if not trains:
        printPretty("원하는 시간대에 배차가 없습니다. 입력하신 시간을 수정해주세요")
        shutdown()

    reserv_targets = []
    for tr in trains:
        depart_time = bs(str(tr), "html.parser").find('input', attrs={"name": regx.compile("dptTm*")})['value'] #regular expression
        if int(time_min.ljust(6,'0')) > int(depart_time) or int(depart_time) > int(time_max.ljust(6,'0')):
            print("depart_time:"+depart_time+"은 예약대상이 아닙니다..")
            continue
        td_list = bs(str(tr), "html.parser").select('td')
        if "매진" not in str(td_list[6]):
            print("예약가능: {}, {}".format(td_list[3], td_list[4]))
            reserv_targets.append(tr)
    return reserv_targets


def finding_seats_param(start, dest, date):
    return {
        'chtnDvCd': '1',
        'isRequest': 'Y',
        'psgInfoPerPrnb1': '1',
        'psgInfoPerPrnb2': '0',
        'psgInfoPerPrnb3': '0',
        'psgInfoPerPrnb4': '0',
        'psgInfoPerPrnb5': '0',
        'psgNum': '1',
        'seatAttCd': '015',
        'stlbTrnClsfCd': '05',
        'trnGpCd': '300',  # 300으로 하면 srt만 나옴, 109는 상관없이 다.
        'arvRsStnCdNm': dest,
        'arvRsStnCd': meta.station_meta_info[dest],
        'dptRsStnCdNm': start,
        'dptRsStnCd': meta.station_meta_info[start],
        'dptDt': date,
        'dptTm': time_min + '0000'
    }


def validate_setting_info():
    stations = meta.station_meta_info.keys()
    if (depart_station not in stations) or (arrive_station not in stations):
        printPretty("역 정보가 올바르지 않습니다. 다시 입력하세요")
        sys.exit(1)
    if int(time_min) > int(time_max):
        printPretty("예약 희망 시간대가 비정상적입니다. 다시 입력하세요")
        sys.exit(1)


def printPretty(msg):
    print("************ [ {} ] ************".format(msg))


def shutdown():
    sys.exit(1)


def announce_success():
    mixer.init()
    mixer.music.load('gunshot.mp3')
    # wait for load
    time.sleep(1)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)
    print("done")


######################################################################
#########################    MAIN LOGIC    ###########################
######################################################################

validate_setting_info()

if not login(id, pw):
    printPretty("login fail")
    shutdown()

printPretty("login success")

isRight = input("출발역 = %s, 도착역 = %s, 예약하고자 하는 날짜 = %s, 희망시간대는 %s ~ %s 맞나요?(y/n):"%(depart_station, arrive_station, reserve_date, time_min, time_max))
if (isRight.lower() != 'y') and (isRight.upper() != 'Y'):
    shutdown()

while True:
    try:
        reserv_targets = find_empty_seats(depart_station, arrive_station, reserve_date, time_min, time_max)
        if len(reserv_targets) > 0 and reserve(reserv_targets):
            break
    except Exception as error:
        print(error)
        if not login(id, pw):
            printPretty("login fail")
            shutdown()
    time.sleep(check_time_term)

printPretty("end")
announce_success()
