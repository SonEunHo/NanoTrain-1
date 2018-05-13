# -*- emcoding: utf8 -*-
import requests
import time
import sys

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
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

login_referer = "https://etk.srail.co.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000"
reserve_referer = "https://etk.srail.co.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000"

reserve_param = {
    'arvRsStnCd1': '0015',
    'arvStnConsOrdr1': '000014',
    'arvStnRunOrdr1': '000004',
    'crossYn': 'N',
    'dirSeatAttCd1': '000',
    'dptDt1': '20180525',
    'dptRsStnCd1': '0551',
    'dptStnConsOrdr1': '000001',
    'dptStnRunOrdr1': '000001',
    'dptTm1': '200000',
    'etcSeatAttCd1': '000',
    'jobId': '1101',
    'jrnyCnt': '1',
    'jrnySqno1': '001',
    'jrnyTpCd': '11',
    'locSeatAttCd1': '000',
    'mutMrkVrfCd': None,
    'psgGridcnt': '1',
    'psgInfoPerPrnb1': '1',
    'psgInfoPerPrnb2': None,
    'psgInfoPerPrnb3': None,
    'psgInfoPerPrnb4': None,
    'psgInfoPerPrnb5': None,
    'psgTpCd1': '1',
    'psgTpCd2': None,
    'psgTpCd3': None,
    'psgTpCd4': None,
    'psgTpCd5': None,
    'psrmClCd1': '1',
    'reqTime': '1526195770894',
    'rqSeatAttCd1': '015',
    'rsvTpCd': '01',
    'runDt1': '20180525',
    'scarGridcnt1': None,
    'scarNo1': None,
    'scarYn1': 'N',
    'seatNo1_1': None,
    'seatNo1_2': None,
    'seatNo1_3': None,
    'seatNo1_4': None,
    'seatNo1_5': None,
    'seatNo1_6': None,
    'seatNo1_7': None,
    'seatNo1_8': None,
    'seatNo1_9': None,
    'smkSeatAttCd1': '000',
    'stlbTrnClsfCd1': '17',
    'stndFlg': 'N',
    'totPrnb': '1',
    'trnGpCd1': '300',
    'trnNo1': '00369',
    'trnOrdrNo1': '6'
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
def checkSeat():
    print ("")

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

# session_etk = ""
#
# response = requests.post('https://etk.srail.co.kr/hpg/hra/01/selectMapInfo.do?isAll=Y&other=&target=dpt&pageId=TK0101010000', headers = common_header, params = param)
# print(response.status_code)


temp = """

검색 -> 예매하기 -> 좌석 고르기 -> 결

cookie : JSESSESIONID, PCID, RC_COLOR, RC_RESOLUTION

지역 코드
몇시차, 인원, 좌석위치

var srt = ['0514', '0036', '0507', '0037', '0010', '0015', '0552', '0041', '0020', '0551', '0508', '0297', '0509', '0030', '0033', '0553', '0502'];
<ul>
						<li><a href="#none" onclick="selectStnCd(this, '0551', '수서'); return false;" class="map-01">수서</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0552', '동탄'); return false;" class="map-02">동탄</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0553', '지제'); return false;" class="map-03">지제</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0502', '천안아산'); return false;" class="map-04">천안아산</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0297', '오송'); return false;" class="map-05">오송</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0010', '대전'); return false;" class="map-06">대전</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0507', '김천구미'); return false;" class="map-07">김천구미</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0015', '동대구'); return false;" class="map-08">동대구</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0508', '신경주'); return false;" class="map-09">신경주</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0509', '울산'); return false;" class="map-10">울산</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0020', '부산'); return false;" class="map-11">부산</a></li>
					</ul>
				</li>
				<li>호남고속선
					<ul>
						<li>수서</li>
						<li>동탄</li>
						<li>지제</li>
						<li>천안아산</li>
						<li>오송</li>
						<li><a href="#none" onclick="selectStnCd(this, '0514', '공주'); return false;" class="map-12">공주</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0030', '익산'); return false;" class="map-14">익산</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0033', '정읍'); return false;" class="map-15">정읍</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0036', '광주송정'); return false;" class="map-16">광주송정</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0037', '나주'); return false;" class="map-17">나주</a></li>
						<li><a href="#none" onclick="selectStnCd(this, '0041', '목포'); return false;" class="map-18">목포</a></li>


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


    <select name="locSeatAttCd1" class="prnb checkForm" option="{isMust : false, message : '좌석위치를 선택하십시오.'}" title="좌석위치 선택">
        <option value="000" selected="selected">좌석위치</option>
        <option value="011">1인석</option>
        <option value="012">창측좌석</option>
        <option value="013">내측좌석</option>
    </select>
    <select name="rqSeatAttCd1" class="prnb checkForm" option="{isMust : false, message : '좌석속성을 선택하십시오.'}" title="좌석속성 선택">
        <option value="015">좌석속성</option>
        <option value="015" selected="selected">일반</option>
        <option value="021">휠체어</option>
        <option value="028">전동휠체어</option>
    </select>
    
    

"""

