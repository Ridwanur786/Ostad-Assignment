import json
import os
from datetime import datetime
import requests


current_data = None

#fetch current weather report for Chattogram

def weather_report():
   global current_data
   native_city = input("Enter your City Name: ").strip()

   if not native_city:
      print("city name required")
      return
   
   wtt_url=f"https://wttr.in/{native_city}?format=j1"

   try:
        response = requests.get(wtt_url, headers={"User-agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        data= response.json()

        current_condition = data['current_condition'][0]

        current_datetime = datetime.now()
        json_time = current_datetime.strftime("%Y-%m-%d %I:%M:%S %p")
        formatted_local_time = current_datetime.strftime( "%Y-%m-%d %I:%M %p")

        print("\n" + "-" *15 + "Weather Report" + "-" * 15)
        print(f"City: {native_city.title()}")
        print(f"Temperature: {current_condition['temp_C']}°C")
        print(f"Weather : {current_condition['weatherDesc'][0]['value']}")
        print(f"Humidity : {current_condition['humidity']} %")
        print(f"Wind Speed : {current_condition['windspeedKmph']} kmp/h")
        print(f"Fetched_at : {formatted_local_time}")
        print("-" * 40 + "\n")

        current_data = {
           "type":"weather",
           "city": native_city.title(),
           "temperature": current_condition['temp_C'],
           "weather": current_condition['weatherDesc'][0]['value'],
           "humidity": current_condition['humidity'],
           "wind_speed": current_condition['windspeedKmph'],
           "fetched_at": json_time
       }


   except Exception as e:
       print(f"there is an error while fatching weather report for {native_city}")

#  -----Real time currency Exchange rate fetcher-----


def currency_rate_fetcher():
    global current_data

    base_currency = input("enter the base currency: ").strip().upper()
    target_C = input("enter target currency: ").strip().upper()

    if not base_currency or not target_C:
        print("empty field cnnot fetch data")
        return

    currency_url = f"https://open.er-api.com/v6/latest/{base_currency}"

    try:
        response= requests.get(currency_url,headers={"User-agent": "Mozilla/5.0"}
         )

        response.raise_for_status()

        data =response.json()

        if data.get("result") == "error":
            print(f"\nError: Invalid '{base_currency}'Code.")
            return
        rates = data.get("rates",{})
        if target_C not in rates:
            print(f"\nError: Target currency '{target_C}' not found for base currency '{base_currency}'.")
            return

        rate =rates[target_C]

        current_datetime = datetime.now()
        json_time = current_datetime.strftime("%Y-%m-%d %I:%M:%S %p")
        formatted_local_time = current_datetime.strftime( "%Y-%m-%d %I:%M %p")

        print("\n" + "-" *15 + "Current Rate" + "-" * 15)
        print(f"\n 1 {base_currency} = {rate} {target_C}")
        print(f"Fetched At: {formatted_local_time}")
        print("-" * 40 + "\n")

        current_data = {
                   "type":"currency",
                   "currency": base_currency.title(),
                   "target_c": target_C.title(),
                   "rate": rate,
                   "fetched_at": json_time
               }
    except Exception as e:
               print(f"\nError Fetching Currency Data: {e}")

def save_json_to_file():
     global current_data

     if current_data is None:
          print("\nError: No Currency or Wearther data to save.")
          return

     try:
          with open("data.json", "w", encoding="utf-8") as file:
              json.dump(current_data,file, indent=4)
              print("\nData Saved Successfully")
     except Exception as e:
          print(f"\nError: saving data:{e}")

def display_saved_data():
     file_name = "data.json"

     if not os.path.exists(file_name):
          print(f"\nError:{file_name} not found.")
          return
     try:
          with open(file_name, "r", encoding="utf-8") as file:
               data = json.load(file)

               print("\nLast Saved Data")

               if data.get("type") == "weather":
                    print("Type: Weather")
                    print(f"City: {data.get('city')}")
                    print(f"Temperature: {data.get('temperature')} °C")
                    print(f"Weather: {data.get('weather')}")
                    print(f"Humidity: {data.get('humidity')}")
                    print(f"Wind Speed: {data.get('wind_speed')} kmp/h")
                    print(f"Fetched At: {data.get('fetched_at')}")

               elif data.get("type") == "currency":
                    print("Type: Currency")
                    print(f"Currency: {data.get('currency')}")
                    print(f"Target: {data.get('target_c')}")
                    print(
                    f"Exchange Rate: 1 {data.get('currency')} = {data.get('rate')} {data.get('target_c')}"
                    )
                    print(f"Fetched At: {data.get('fetched_at')}")
               else:
                    print("\nError data type in json file")
     except json.JSONDecodeError:
        print("\nError: data.json file contains invalid JSON data.")
     except Exception as e:
        print(f"\nError reading file: {e}")   

def menu():
     #***dispaly main menu in CLI***
    while True:
         print("\n======DATA FEATCHER MENU=====")
         print("1.Weather Report")        
         print("2.Currency Exchange rate")        
         print("3.Save Data to data.json")        
         print("4.View Previously Saved Data")        
         print("5.Exit")   
         print("=================================")

         options = input("Choose your options: ")

         if options == "1":
              weather_report()
         elif options == "2":
              currency_rate_fetcher()
         elif options == "3":
              save_json_to_file()
         elif options == "4":
              display_saved_data()
         elif options == "5":
              print("\n GOODBYE!!")
              break
         else:
            print("\nInvalid choice! Please enter a number between 1 and 5.")              



       
if __name__ == "__main__":
    menu()


        
