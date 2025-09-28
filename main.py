import sys
import requests
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class weather(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name : ",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("getweather",self)
        self.temp_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self) 
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #000000;
                font-family: Calibri, Arial, sans-serif;
            }

            QLabel {
                font-size: 20px;
                color: #000000;
            }

            QLabel#temp_label {
                font-size: 48px;
                font-weight: bold;
                color: #000000;
            }

            QLabel#emoji_label {
                font-family: Apple Color Emoji;
                font-size: 64px;
            }

            QLabel#description_label {
                font-size: 24px;
                color: #000000;
            }

            QLabel#city_label {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 5px;
            }

            QLineEdit#city_input {
                font-size: 20px;
                padding: 8px;
                border-radius: 10px;
                border: 2px solid #444;
                background-color: #ffffff;
                color: #000000;
            }

            QPushButton#get_weather_button {
                font-size: 22px;
                padding: 10px;
                border-radius: 12px;
                border: 2px solid #444;
                background-color: #ffffff;
                color: #000000;
            }

            QPushButton#get_weather_button:hover {
                background-color: #ffffff;
                color: #000000;
                font-weight: bold;
            }
        """)
        self.get_weather_button.clicked.connect(self.getWeather)


    def getWeather(self):
        api_key = "05798580cf6bb913e17852e59d6142a8"

        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        
        try:
            responce = requests.get(url)
            responce.raise_for_status()
            data = responce.json()
            print(data)
            if(data["cod"] == 200):
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match responce.status_code:
                case 400:
                    self.display_error("bad request\n please check your input")
                case 401:
                    self.display_error("unauthorised\n invalid api key")
                case 403:
                    self.display_error("foebidden\n access denied")
                case 404:
                    self.display_error("not found\ncity not found ")
                case 500:
                    self.display_error("internal server error\n please try again later")
                case 502:
                    self.display_error("bad gateway\ninvalid responce from the server")
                case 503:
                    self.display_error("service is unAvailable\n server is down")
                case 504:
                    self.display_error("gateWay timeout\n  no responce from the server")
                case _:
                    self.display_error(f"HTTPError occured\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("connection Error:\n check your connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\n the request timeout")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\n check the URL")
        except requests.exceptions.RequestException as reqError:
            self.display_error(f"RequestError\n{reqError}")

    def display_error(self,message):
        self.temp_label.setStyleSheet("")
        self.temp_label.setText(message)

    def display_weather(self,data):

        temprature_celcious = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        self.description_label.setText(desc.capitalize())
        self.temp_label.setText(f"{temprature_celcious:.1f}°C")
        weather_main = data["weather"][0]["main"]
        weatherId = data['weather'][0]['id']
        self.emoji_label.setText(self.get_weather_emoji(weatherId))
    
    @staticmethod
    def get_weather_emoji(weatherId):
                if 200 <= weatherId <= 232:
                    return "⛈️"  # Thunderstorm
                elif 300 <= weatherId <= 321:
                    return "🌦️"  # Drizzle
                elif 500 <= weatherId <= 531:
                    return "🌧️"  # Rain
                elif 600 <= weatherId <= 622:
                    return "❄️"  # Snow
                elif 701 <= weatherId <= 781:
                    return "🌫️"  # Mist, Smoke, Haze, etc.
                elif weatherId == 800:
                    return "☀️"  # Clear
                elif 801 <= weatherId <= 804:
                    return "☁️"  # Clouds
                else:
                    return "🌍"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherApp = weather()
    weatherApp.show()
    sys.exit(app.exec_())
