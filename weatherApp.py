import sys
import requests
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(800, 315, 325, 450)

        vboxLayout = QVBoxLayout()
        self.setLayout(vboxLayout)
        vboxLayout.addWidget(self.city_label)
        vboxLayout.addWidget(self.city_input)
        vboxLayout.addWidget(self.get_weather_button)
        vboxLayout.addWidget(self.temperature_label)
        vboxLayout.addWidget(self.emoji_label)
        vboxLayout.addWidget(self.description_label)

        all_labels = [self.city_label, self.temperature_label, self.emoji_label, self.description_label]
        for label in all_labels:
            label.setAlignment(Qt.AlignCenter)

        self.emoji_label.setObjectName("emoji_label")
        self.city_input.setObjectName("city_input")

        self.setStyleSheet("""
            QLabel{
                font-size: 40px;
                font-family: Arial;
            }
            QPushButton{
                font-size: 30px;
                font-family: Verdana;
            }
            QLineEdit{
                font-size: 30px;
            }
            
            QLabel#emoji_label{
                background-color: #e3e3e3;            
            }
        """)

        self.get_weather_button.clicked.connect(self.updateData)
        self.timer.timeout.connect(self.activate_button)

    def updateData(self):
        self.get_weather_button.setDisabled(True)
        self.timer.start(3000)
        data = self.get_weather_data()

        if data is not None:
            self.temperature_label.setText(f"{int(data['main']['temp'] - 273.15)}°C")
            self.emoji_label.setPixmap(self.get_icon(data["weather"][0]["icon"]))
            self.description_label.setText(data["weather"][0]["description"].capitalize())
        else:
            self.temperature_label.setText("City name is wrong!")
            self.description_label.setText(" Please enter a valid city😊")

    def get_icon(self, icon_id):
        url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
        response = requests.get(url)

        if response.status_code == 200:
            icon_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)
            return pixmap
        else:
            return None

    def get_weather_data(self):
        coordinates = self.get_coordinates()

        if coordinates is None:
            return None

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates['lat']}&lon={coordinates['lon']}&appid=6965e8a46ac893ef26d076af9bbb214b"
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            return None

    def get_coordinates(self):

        city = self.city_input.text().strip()
        if not city:
            self.temperature_label.setText("Please Enter a city name!")
            return None

        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid=6965e8a46ac893ef26d076af9bbb214b"
        response = requests.get(url)

        if response.status_code == 200:
            coordinate_data = response.json()

            if not coordinate_data:
                return None

            lat = coordinate_data[0]["lat"]
            lon = coordinate_data[0]["lon"]

            return {"lat": lat,
                    "lon": lon}
        else:
            return None


    def activate_button(self):
        self.get_weather_button.setDisabled(False)
        self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather = WeatherApp()
    weather.show()
    sys.exit(app.exec_())
