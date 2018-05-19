# -*- encoding: utf8 -*-
import requests
import time
import sys
from bs4 import BeautifulSoup as bs
#계정 : 1584314147

my_cookie = {
    'JSESSIONID_ETK': '9TlJyAnoWpw33CTnx1f0yprb10fmr1fTA1vIIrf3UGZaX1e1MXNvjZjAIdSOBXTT',
    'PCID': '15261430919745926997128',
    'RC_COLOR': '24',
    'RC_RESOLUTION': '1680*1050'
}

station = {
    "공주": '0514',
    "광주송정": '0036',
    '김천구미': '0507',
    '나주': '0037',
    '대전': '0010',
    '동대구': '0015',
    '동탄': '0552',
    '목포': '0041',
    '부산': '0020',
    '수서': '0551',
    '신경주': '0508',
    '오송': '0297',
    '울산': '0509',
    '익산': '0030',
    '정읍': '0033',
    '지제': '0553',
    '천안아산': '0502'
}

param = {
    "dptRsStnCd": '0551',
    "arvRsStnCd": '0020',
    "stlbTrnClsfCd": '05',
    "psgNum": '1',
    "seatAttCd": '015',
    "isRequest": 'Y',
    "dptRsStnCdNm": '수서',
    "arvRsStnCdNm": '부산',
    "dptDt": '20180513',
    "dptTm": '005000',
    "chtnDvCd": '1',
    "psgInfoPerPrnb1": '1',
    "psgInfoPerPrnb5": '0',
    "psgInfoPerPrnb4": '0',
    "psgInfoPerPrnb2": '0',
    "psgInfoPerPrnb3": '0',
    "locSeatAttCd1": '000',
    "rqSeatAttCd1": '015',
    "trnGpCd": '109'
}

common_header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Cookie": "PCID=15254283299465733307147; RC_COLOR=24; JSESSIONID_ETK=9TlJyAnoWpw33CTnx1f0yprb10fmr1fTA1vIIrf3UGZaX1e1MXNvjZjAIdSOBXTT; RC_RESOLUTION=1920*1080",
    "Host": "etk.srail.co.kr",
    "Referer": "https://etk.srail.co.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0"
}

login_referer = "https://etk.srail.co.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000"
reserve_referer = "https://etk.srail.co.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000"

reserve_param = {
    'arvRsStnCd1': '0015', #도착역 코드
    'arvStnConsOrdr1': '000014', #tr에 있음
    'arvStnRunOrdr1': '000004', #tr에 있음
    'crossYn': 'N', # ????
    'dirSeatAttCd1': '000', #tr에 있음
    'dptDt1': '20180525', #날짜
    'dptRsStnCd1': '0551', #출발역 코드
    'dptStnConsOrdr1': '000001', #tr에 있음
    'dptStnRunOrdr1': '000001', #tr에 있음
    'dptTm1': '200000', #tr에 있음
    'etcSeatAttCd1': '000', #??
    'jobId': '1101', #고정인
    'jrnyCnt': '1', #고정인듯
    'jrnySqno1': '001', #tr에 있음
    'jrnyTpCd': '11', #??? 고정인듯
    'locSeatAttCd1': '000', #좌석위치 (조회시 내가 날림)
    'mutMrkVrfCd': None, #???
    'psgGridcnt': '1', #사람수??
    'psgInfoPerPrnb1': '1', #어른
    'psgInfoPerPrnb2': None, #장애인(1~3급)
    'psgInfoPerPrnb3': None, #장애인(4~6급)
    'psgInfoPerPrnb4': None, #노인
    'psgInfoPerPrnb5': None, #얼라
    'psgTpCd1': '1', #어른
    'psgTpCd2': None, #장애인 1~3급
    'psgTpCd3': None, #장애인(4~6급)
    'psgTpCd4': None, #노인
    'psgTpCd5': None, #얼라
    'psrmClCd1': '1', #???
    'reqTime': '1526195770894', #현재 시간
    'rqSeatAttCd1': '015', #좌석 속성 (일반015 / 휠체어 021 / 전동휠체어 028)
    'rsvTpCd': '01', #???
    'runDt1': '20180525', #날
    'scarGridcnt1': None, #???
    'scarNo1': None, #???
    'scarYn1': 'N', #???
    'seatNo1_1': None, #tr안에 있음
    'seatNo1_2': None, #tr안에 있음
    'seatNo1_3': None, #tr안에 있음
    'seatNo1_4': None, #tr안에 있음
    'seatNo1_5': None, #tr안에 있음
    'seatNo1_6': None, #tr안에 있음
    'seatNo1_7': None, #tr안에 있음
    'seatNo1_8': None, #tr안에 있음
    'seatNo1_9': None, #tr안에 있음
    'smkSeatAttCd1': '000', #???
    'stlbTrnClsfCd1': '17', #tr에 있
    'stndFlg': 'N', #??? 입석?
    'totPrnb': '1', #총 사람 수
    'trnGpCd1': '300', #기차 종류 (300: srt)
    'trnNo1': '00369', #기차번호
    'trnOrdrNo1': '6' #???
}


def login(id, pw):
    header = common_header.copy()
    header["Referer"] = login_referer
    header['Content-Type'] = 'application/x-www-form-urlencoded'

    param = {
        'rsvTpCd': None,
        'goUrl': None,
        'from': None,
        'srchDvCd': '1',
        'srchDvNm': id,
        'hmpgPwdCphd': pw
    }
    r = requests.post('https://etk.srail.co.kr/cmc/01/selectLoginInfo.do?pageId=TK0701000000', headers = header, params = param)

    if '오류' in r.text:
        return 400
    elif '실패' in r.text:
        return 400
    elif 'location.replace(\'/main.do\')' in r.text:
        return 200

#예약하기
def reserve():
    req_time = int(time.time()*1000)
    print ("")

#빈 좌석이 있는지 확인
# 있으면 시간, 좌석정보(가능할까) 반환
def checkSeat(start, dest, date, time_min = '000000', time_max = '220000'):
    header = dict(common_header)
    del header['Cookie'] #쿠키 값을 없애도 정상 응답이 온다.
    header["Referer"] = "https://etk.srail.co.kr/main.do"
    header['Content-Type'] = 'application/x-www-form-urlencoded'

    param = {
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
        'trnGpCd': '300' #300으로 하면 srt만 나옴, 109는 상관없이 다.
    }
    param['arvRsStnCdNm'] = dest
    param['arvRsStnCd'] = station[dest]
    param['dptRsStnCdNm'] = start
    param['dptRsStnCd'] = station[start]
    param['dptDt'] = date
    param['dptTm'] = time_min+'0000'

    print(header)
    response = requests.post("https://etk.srail.co.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000", headers = header, params = param)

    #열차 정보만 가져온다.
    tr_list = bs(response.text, 'html.parser').select("tbody > tr")

    for tr in tr_list:
        print("="*20)
        td_list = bs(str(tr), "html.parser").select('td')
        if "매진" not in str(td_list[6]):
            print("예약가능: {}, {}".format(td_list[3], td_list[4]))

def pay():
    print("pay")

def getSessionETK():
    response = requests.get("https://etk.srail.co.kr/")
    print (response.cookies.get_dict())
    if response.status_code == 200:
        return response.cookies['JSESSIONID_ETK']
    else:
        return "-1"

check_time_term = "3" #3초에 한번 확인


######################################################################
######################################################################
######################################################################
######################################################################
######################################################################

id = input("id입력:")
pw = input("pw입력:")

if login(id, pw)!=200:
    print("----login fail----")
    sys.exit(1)

print ("----login success----")

## 열차 빈 좌석 확인
stations = station.keys()
while True:
    print ("역정보:"+str(stations))
    start_station = input("출발역을 입력하세요:")
    dest_station = input("도착역을 입력하세요:")

    if (start_station in stations) and (dest_station in stations):
        break
    print("역 정보가 올바르지 않습니다. 다시 입력하세요")

while True:
    date = input("승차할 날짜를 입력하세요 (ex. 20180515) ('-'포함금지) :")
    print("승차하고자 하는 시간대를 입력해주세요 (ex 14시~16시)")
    time_min = input("승차하고자 하는 가장 빠른 시간을 입력해주세요:")
    time_max = input("승차하고자 하는 가장 늦은 시간을 입력해주세요:")
    isRight = input("date = %s, 희망시간대는 %s ~ %s 맞나요?(y/n):"%(date, time_min, time_max))
    if isRight.lower() == 'y':
        break;

print("date = %s, 희망시간대는 %s ~ %s 로 열차를 검색하기 시작합니다" %(date, time_min, time_max))

while True:
    checkSeat(start_station, dest_station, date, time_min, time_max)
    #예약 성공하면 종료
    break;




temp = """

검색 -> 예매하기 -> 좌석 고르기 -> 결

cookie : JSESSESIONID, PCID, RC_COLOR, RC_RESOLUTION

도착역 코드    arvRsStnCd	0015
도착역 이름    arvRsStnCdNm	동대구
???    chtnDvCd	1
출발날짜    dptDt	20180507
출발역 코드    dptRsStnCd	0551
출발역 이    dptRsStnCdNm	수서
출발시간    dptTm	150500
리퀘스트인지..    isRequest	Y (불변)
사람수(어른)    psgInfoPerPrnb1	1
사람수(장애 1~3급)    psgInfoPerPrnb2	0
사람수(장애 4~6급)    psgInfoPerPrnb3	0
사람수(만65세 이상)    psgInfoPerPrnb4	0
사람수(만4세~12세)   psgInfoPerPrnb5	0
사람수(종합)    psgNum	1  (종합 수는 9명 이하여야한다.)
좌석속성    rqSeatAttCd1 015  (일반015 / 휠체어 021 / 전동휠체어 028)
좌석위    seatAttCd	015 (암때나 015 / 1인석 011/ 창측좌석 012 / 내측좌석 013) 
???    stlbTrnClsfCd	05
차종구분    trnGpCd	109 (전체 109 / SRT 300 / SRT+KTX 900)

승차권종류 : pageId	TK0101010000 (일반승차권 TK0101010000 / 단체승차권 TK0101020000)
"""

