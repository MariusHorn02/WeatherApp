import sys
import os
import requests

from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

load_dotenv()

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather", self)
        self.temperature_label = QLabel( self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel( self)
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Weather APP")

        vBox = QVBoxLayout()

        vBox.addWidget(self.city_label)
        vBox.addWidget(self.city_input)
        vBox.addWidget(self.get_weather_button)
        vBox.addWidget(self.temperature_label)
        vBox.addWidget(self.emoji_label)
        vBox.addWidget(self.description_label)

        self.setLayout(vBox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
                           QLabel, QPushButton{
                           font_family: calibri;
                           }
                           QLabel#city_label{
                           font-size: 40px;
                           font-style: italic;

                           }
                           QLineEdit#city_input{
                           font-size: 40px;
                           min-height: 50px;
                           }
                           QPushButton#get_weather_button{
                           font-size: 30px;
                           font-weight: bold;
                           }
                           QLabel#temperature_label{
                           font-size: 75px;
                           }
                           QLabel#emoji_label{
                           font-size: 100px;
                           font-family: "Apple Color Emoji", "Segoe UI Emoji";
                           }
                           QLabel#description_label{
                           font-size: 50px;
                           }
                           """)
        

        self.get_weather_button.clicked.connect(self.get_weather)




    def get_weather(self):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            self.display_error("Missing API key.\nSet OPENWEATHER_API_KEY in .env")
            return

        city = self.city_input.text().strip()
        if not city:
            self.display_error("Please enter a city.")
            return

        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": api_key, "units": "metric"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            self.display_weather(data)

        except requests.exceptions.HTTPError as e:
            status = response.status_code if "response" in locals() else None
            if status == 400:
                self.display_error("Bad request:\nPlease check your input")
            elif status == 401:
                self.display_error("Unauthorized:\nInvalid API key")
            elif status == 403:
                self.display_error("Forbidden:\nAccess is denied")
            elif status == 404:
                self.display_error("Not found:\nCity not found")
            elif status == 500:
                self.display_error("Internal server error:\nTry again later")
            elif status == 502:
                self.display_error("Bad gateway:\nInvalid response from server")
            elif status == 503:
                self.display_error("Service unavailable:\nServer is down")
            elif status == 504:
                self.display_error("Gateway timeout:\nNo response from server")
            else:
                self.display_error(f"HTTP error:\n{e}")

        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nThe request timed out")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nCheck your internet connection")

        except requests.exceptions.RequestException as e:
            self.display_error(f"Request error:\n{e}")


    def display_error(self, message):

        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")

        temperature_c = data["main"]["temp"]  # already Celsius because units=metric
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c:.0f}° C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <=232:
            return "⛈️"
        elif 300 <= weather_id <=321:
            return "☁️"
        elif 500 <= weather_id <=531:
            return "🌧️"
        elif 600 <= weather_id <=622:
            return "❄️"
        elif 701 <= weather_id <=741:
            return "🌁"
        elif weather_id ==762:
            return "🌋"
        elif weather_id ==771:
            return "💨"
        elif weather_id ==781:
            return "🌪️"
        elif weather_id ==800:
            return "☀️"
        elif 801 <= weather_id <=804:
            return "☁️"
        else:
            return " "
            
        
        
        





if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())



