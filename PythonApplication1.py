import requests
import xml.etree.ElementTree as ET
import codecs
from datetime import datetime

# 사용자로부터 서비스 키 입력
service_key = 'Your_Key'

#현재시각 = datetime
now = datetime.now()

# 시각을 "연연연연월월일일" 형식의 문자열로 변환
today =datetime.today().strftime('%Y%m%d')

# API 엔드포인트 및 요청 매개변수 설정
url = 'http://apis.data.go.kr/1360000/EqkInfoService/getEqkMsg'
params = {
    'serviceKey': service_key,
    'pageNo': '1',
    'numOfRows': '1',  # 1개의 결과만 가져옴
    'dataType': 'XML',
    'fromTmFc': int(today)-1,  # 오늘의 날짜로 설정
    'toTmFc': today,    # 오늘의 날짜로 설정
}

# API를 호출하고 응답을 가져옴
response = requests.get(url, params=params)
# API 응답을 확인하고 디코드하여 출력

if response.status_code == 200:
    # API에서 반환한 XML 데이터를 가져옴
    xml_data = response.content
    # XML 파싱
    root = ET.fromstring(xml_data)

    # 원하는 정보 추출
    headers = root.find('.//header')
    items = root.find('.//items')
    if headers is not None:
        if items is not None:
            for item in items.findall('.//item'):
                fcTp = item.find('fcTp').text
                img = item.find('img').text
                tmFc = item.find('tmFc').text
                tmSeq = item.find('tmSeq').text
                cnt = item.find('cnt').text
                tmEqk = item.find('tmEqk').text
                lat = item.find('lat').text
                loc = item.find('loc').text
                lon = item.find('lon').text
                rem = item.find('rem').text

                output = f"# : {cnt}, fcTp : {fcTp}, img : {img}, tmFc : {tmFc}, tmSeq : {tmSeq}, cnt : {cnt}, tmEqk : {tmEqk}, lat : {lat}, lon : {lon}, 진앙 위치 : {loc}, 참고사항 : {rem}"

                if 'stnId' in item.attrib:
                    stnId = item.find('stnId').text
                    output += f", stnId : {stnId}"

                if 'mt' in item.attrib:
                    mt = item.find('mt').text
                    output += f", 규모 : {mt}"

                if 'inT' in item.attrib:
                    inT = item.find('inT').text
                    output += f", 진도 : {inT}"

                if 'dep' in item.attrib:
                    dep = item.find('dep').text
                    output += f", 깊이 : {dep}"
                    
                if 'cor' in item.attrib:
                    cor = item.find('cor').text
                    output += f", 수정 사항 : {cor}"
                print(output)
        else:
            for header in headers.findall('.//header'):
                rst = headers.find('resultCode').text
                sts = headers.find('resultMsg').text
                print(f"에러코드 {rst}로 인해 정보를 받지 못했습니다. 에러사유 : {sts}")
                print(xml_data)
else:
    print(f"API 호출 실패: {response.status_code}")
