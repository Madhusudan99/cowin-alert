import requests
import json
import time
from datetime import datetime
from playsound import playsound

class Availability:
    def __init__(self, pincode, date, age):
        self.age = age
        self.payload = {'pincode': pincode, 'date': date}
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        self.r = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin", headers=self.headers, params=self.payload)
    
    def get_details(self):
        print(f'URL: {self.r.url}')
        print(f'STATUS: {self.r.status_code}')
        print(f'Text: \n{self.r.text}')
        return {'URL': self.r.url, 'STATUS': self.r.status_code, 'Text': self.r.text}
    
    def dump_JSON(self):
        with open("vaccine.json", "w") as f:
            json.dump(self.r.json(), f, indent=4)
    
    def alert(self):
        data = json.loads(self.r.text)
        for center in data['centers']:
            for session in center['sessions']:
                if session['min_age_limit'] == self.age and session["available_capacity"] > 0:
                    print(datetime.now())
                    print(f'{center["name"]}    {session["available_capacity"]}')
                    # Prints a # pattern 
                    for i in range(5):
                        for j in range(100):
                            print("#", end="")
                        print()
                    return True
        return False
    
    def checking_loop(self, timer):
        counter = 1
        while self.alert() is False:
            print(counter, "NA")
            counter += 1
            time.sleep(timer)
        playsound("alaram.wav")


if __name__ == '__main__':
    vaccine = Availability(pincode='364002', date='10-05-2021', age=18)
    # vaccine.get_details()
    vaccine.checking_loop(timer=5)