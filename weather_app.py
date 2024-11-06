import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  
import geocoder


def get_location():
    try:
        location = geocoder.ip('me')
        if location.city:
            return location.city
        else:
            return "Location not found:"
    except Exception as e:
        print("Error detecting location:", e)
        return "Location not found"


def get_weather(city, unit):
    api_key = "cea48bdc21a9473299701605243010"  
    base_url = "http://api.weatherapi.com/v1/current.json"
    
    params = {
        "key": api_key,
        "q": city,
        "days": 5,
        "aqi": "no"
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    print("API Response Data:", data)

    if "forecast" not in data:
        print("Error: Forecast data is missing.")
        if "error" in data:
            print("API Error Message:", data["error"].get("message", "No error message provided"))
        return "Forecast data not available.", None 


    if response.status_code == 200:
        current_weather = data["current"]
        forecast_days = data["forecast"]["forecastday"]

        temperature = data["current"]["temp_f"] if unit == "Fahrenheit" else data["current"]["temp_c"]
        description = data["current"]["condition"]["text"].lower()
        current_summary = f"{city.capitalize()} - {description.capitalize()}, {temperature}°{unit[0]}"
        icon = get_icon_path(description) 

        forecast = []
        for day in forecast_days:
            date = day["date"]
            day_temp = day["day"]["avgtemp_f"] if unit == "Fahrenheit" else day["day"]["avgtemp_c"]
            condition = day["day"]["condition"]["text"]
            icon = get_icon_path(condition.lower())
            forecast.append((date, condition, day_temp, icon))

        return f"{city.capitalize()} - {description.capitalize()}, {temperature}°{unit[0]}", icon
    else:
        return "City not found or API error.", None  
    

def get_icon_path(description):
    if "sunny" in description:
        return "icons/sunny.png"
    elif "cloud" in description:
        return "icons/cloudy.png"
    elif "rain" in description:
        return "icons/rainy.png"
    elif "snow" in description:
        return "icons/snow.png"
    elif "clear" in description:  
        return "icons/clear.png"
    else:
        return "icons/unknown.png"  



def show_weather():
    city = city_entry.get().strip()
    unit = unit_var.get()
    
    if not city:
        city = detected_city
    
    
    result, forecast = get_weather(city, unit)
    messagebox.showinfo("Current Weather", result)
    
    
    for widget in forecast_frame.winfo_children():
        widget.destroy()
    
    
    if forecast:
        for day in forecast:
            date, condition, temp, icon_path = day
            day_frame = tk.Frame(forecast_frame, bg="#87CEEB")
            day_frame.pack(fill="x", pady=2)
            
            date_label = tk.Label(day_frame, text=date, font=("Arial", 10, "bold"), bg="#87CEEB")
            date_label.pack(side="left", padx=10)
            
            condition_text = f"{condition}, {temp}°{unit[0]}"
            condition_label = tk.Label(day_frame, text=condition_text, font=("Arial", 10), bg="#87CEEB")
            condition_label.pack(side="left", padx=10)
            
            if icon_path:
                try:
                    weather_icon = Image.open(icon_path)
                    weather_icon = weather_icon.resize((30, 30), Image.LANCZOS)
                    weather_image = ImageTk.PhotoImage(weather_icon)
                    
                    icon_label = tk.Label(day_frame, image=weather_image, bg="#87CEEB")
                    icon_label.image = weather_image
                    icon_label.pack(side="left", padx=10)
                except Exception as e:
                    print("Error loading image:", e)
    else:
      
        no_forecast_label = tk.Label(forecast_frame, text="Forecast data is not available.", font=("Arial", 10), bg="#87CEEB")
        no_forecast_label.pack(pady=10)



root = tk.Tk()
root.title("Weather App")
root.geometry("300x300")  
root.configure(bg="#87CEEB")  


detected_city = get_location()
city_entry = tk.Entry(root, width=20, font=("Arial", 14))
city_entry.insert(0, detected_city)
city_entry.pack(pady=10)


unit_var = tk.StringVar(value="Celsius")
unit_menu = tk.OptionMenu(root, unit_var, "Celsius", "Fahrenheit")
unit_menu.config(font=("Arial", 12))
unit_menu.pack(pady=5)


icon_label = tk.Label(root, bg="#87CEEB") 
icon_label.pack(pady=5)

check_weather_button = tk.Button(root, text="Check Weather", command=show_weather, font=("Arial", 12))
check_weather_button.pack(pady=10)

forecast_frame = tk.Frame(root, bg="#87CEEB")
forecast_frame.pack(fill="both", expand=True, pady=10)


root.mainloop()
