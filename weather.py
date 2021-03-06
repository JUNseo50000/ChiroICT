from datetime import datetime 
import requests
from bs4 import BeautifulSoup
import urllib.parse



def get_base_time(hour):
    hour = int(hour)
    if hour < 3:
        temp_hour = '20'
    elif hour < 6:
        temp_hour = '23'
    elif hour < 9:
        temp_hour = '02'
    elif hour < 12:
        temp_hour = '05'
    elif hour < 15: 
        temp_hour = '08' 
    elif hour < 18: 
        temp_hour = '11' 
    elif hour < 21: 
        temp_hour = '14' 
    elif hour < 24: 
        temp_hour = '17' 
    
    return temp_hour + '00'

class weather:
    # todo : try except
    def __init__(self, nx, ny, city, region):
        self.region = region
        now = datetime.now()
        now_date = now.strftime('%Y%m%d')
        now_hour = int(now.strftime('%H'))
        
        # 6시 이전엔 관측 정보가 나오지 않는다.
        if now_hour < 6:
            self.base_date = str(int(now_date) - 1)
        else:
            self.base_date = now_date
        self.base_time = get_base_time(now_hour)
        # 동네예보조회 총 항목 14개, 미세먼지도 14개면 동작구 포함되어 있다.
        num_of_rows = '14'
        self.nx = str(nx)
        self.ny = str(ny)
        _type = 'json'

        weather_service_key = 'YFohKytqZhR5%2FTERmS%2FN8D2hNPsP4l6JOfDAgLxdhPB7l1SJfMjwUSdT83tUT4ABgPaPkGmN3k13HZ4B%2BDM%2B3Q%3D%3D'
        # weather_api_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?serviceKey={weather_service_key}&numOfRows={num_of_rows}&dataType={_type}&pageNo=1&base_date={self.base_date}&base_time={self.base_time}&nx={nx}&ny={ny}'
        # weather_data = urlopen(weather_api_url).read().decode('utf8')
        # self.weather_json_data = json.loads(weather_data)
        weather_api_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?serviceKey={weather_service_key}&numOfRows={num_of_rows}&pageNo=1&base_date={self.base_date}&base_time={self.base_time}&nx={nx}&ny={ny}'
        res = requests.get(weather_api_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        self.weather_data = soup.find_all('item')

        sidoName = urllib.parse.quote_plus(city)
        dust_service_key = 'YFohKytqZhR5%2FTERmS%2FN8D2hNPsP4l6JOfDAgLxdhPB7l1SJfMjwUSdT83tUT4ABgPaPkGmN3k13HZ4B%2BDM%2B3Q%3D%3D'
        dust_api_url = f'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey={dust_service_key}&numOfRows={num_of_rows}&pageNo=1&sidoName={sidoName}&searchCondition=DAILY'

        res = requests.get(dust_api_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        self.dust_data = soup.find_all('item')


    def get_dust(self):
        for item in self.dust_data:
            cityname = item.find('cityname')

            if cityname.get_text() == self.region:
                self.pm10value = int(item.find('pm10value').get_text())
                self.pm25value = int(item.find('pm25value').get_text())
                print(cityname.get_text())
                print('pm10value : ' + item.find('pm10value').get_text())
                print('pm25value : ' + item.find('pm25value').get_text())

    def get_rain(self):
        # 강수형태(PTY) 코드 : 없음(0), 비(1), 진눈개비(2), 눈(3), 소나기(4), 빗방울(5), 빗방울/눈날림(6), 눈날림(7)
        # 강수확률(POP)[%]

        for item in self.weather_data:
            precipitation_type = item.find('category')

            if item.find('category').get_text() == 'PTY':
                self.precipitation_type = int(item.find('fcstvalue').get_text())
                print('PTY : ' + item.find('fcstvalue').get_text() + ' \tAt ' + item.find('fcsttime').get_text())

            if item.find('category').get_text() == 'POP':
                self.precipitation_probability = int(item.find('fcstvalue').get_text())
                print('POP : ' + item.find('fcstvalue').get_text() + ' \tAt ' + item.find('fcsttime').get_text())

    def weatherCheck(self):
        self.get_dust()
        self.get_rain()

        # check rain status
        # 1456 -> 비, 소나기, 빗방울, 빗방울/눈날림

        # todo
        if self.precipitation_type == 1 or self.precipitation_type == 4 or self.precipitation_type == 5 or self.precipitation_type == 6:
            # speak something and open drawer
            pass
        elif self.precipitation_probability >= 50:
            pass
        
        
        # 생각해볼 점. 초미세먼지 미세먼지 둘다 매우나쁨 일때.
        # check dust status
        # 미세먼지 매우나쁨 151~
        if self.pm10value >= 151:
            pass
        # 초미세먼지 매우나쁨 76~
        elif self.pm25value >= 76:
            pass
        # 미세먼지 나쁨 81 ~ 125
        elif self.pm10value >= 81 and self.pm10value <= 150:
            pass
        # 초미세먼지 나쁨 36 ~ 75
        elif self.pm25value >= 36 and self.pm10value <= 75:
            pass
            


# weather(60,125, '서울', '동작구').weatherCheck()
weather = weather(60,125, '서울', '동작구')
weather.weatherCheck()

# weather.get_rain()
# weather.get_dust()