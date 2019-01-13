login_referer = "https://etk.srail.co.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000"
login_request_url = "https://etk.srail.co.kr/cmc/01/selectLoginInfo.do?pageId=TK0701000000"
check_seat_url = "https://etk.srail.co.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000"
temporal_session_id = '9TlJyAnoWpw33CTnx1f0yprb10fmr1fTA1vIIrf3UGZaX1e1MXNvjZjAIdSOBXTT'
reservation_url = "https://etk.srail.co.kr/hpg/hra/01/checkUserInfo.do?pageId=TK0101010000"
reservation_url2 = "https://etk.srail.co.kr/hpg/hra/02/requestReservationInfo.do?pageId=TK0101030000"
reservation_confirm_url = "https://etk.srail.co.kr/hpg/hra/02/confirmReservationInfo.do?pageId=TK0101030000"

my_cookie = {
    'JSESSIONID_ETK': temporal_session_id,
    'PCID': '15261430919745926997128',
    'RC_COLOR': '24',
    'RC_RESOLUTION': '1680*1050'
}

station_meta_info = {
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

common_header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Host": "etk.srail.co.kr",
    "Referer": check_seat_url,
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

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