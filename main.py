from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout
from app_api_key import api_key
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont 

class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.api_key = api_key
        self.submit.clicked.connect(self.search_click)
    
    def settings(self):
        #give app a title
        self.setWindowTitle("Weather!")

        #where do you want the app to appear?
        self.setGeometry(1400, 700, 500, 300)

    def initUI(self): #where design takes place
        #create objects then add objects to a design

        self.title = QLabel("Weather Today!")
        self.title.setFont(QFont("monospace", 20))
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter location") #provide hint to user

        #output field
        self.output = QLabel("Forecast: ")
        self.submit = QPushButton("Search")
        self.submit.setFont(QFont("monospace", 10))
        #create columns for objects
        self.master = QVBoxLayout()
        self.master.addWidget(self.title, alignment=Qt.AlignCenter) #add to screen
        self.master.addWidget(self.input_box)
        self.master.addWidget(self.output)
        self.master.addWidget(self.submit)

        self.setLayout(self.master)

        self.setStyleSheet("""
            QWidget { background-color: #def9fa; }
            QLabel{ color: #d9b1de;}    
            QLineEdit {border: 3px solid #969eb5;padding:5px;}        
            QLabel#output {color: #e6a3d2;}        
            QPushButton{background-color:#f4daf7; color: #b38ab8; border:2px solid #969eb5;}  
            QPushButton:hover{background-color:#a097a1;}
                           """)

    def search_click(self):
        self.result = self.get_weather(self.api_key, self.input_box.text())

        self.output.setText(self.result)


    def get_weather(self, api_key, city, country=""):
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        parameters = {'q': f'{city}, {country}', 'appid': api_key}

        try:
            response = requests.get(base_url, params=parameters)
            data = response.json()

            if response.status_code == 200:
                #if working
                city_name = data['name']
                country_code = data['sys']['country']

                temperature_kelvin = data['main']['temp']
                temperature_fahrenheit = (temperature_kelvin - 273.15) * 1.8 + 32

                weather_description = data['weather'][0]['description']
                humidity = data['main']['humidity']

                weather_information =( f"Weather in {city_name}, {country_code}: \n"
                                       f"Temperature: {temperature_fahrenheit:.2f} °F\n"
                                       f"Humidity: {humidity}%"
                                      
                                      )
                return weather_information
            else:
                return f"Error: {data['message']}"
            
        except Exception as e:
            return f"An error occurred: {e}"

        

if __name__ in "__main__":
    app = QApplication([]) #create app -> give empty list as argument
    main = Home() #main window
    main.show() #show main window
    app.exec_() #run app

