import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


def get_weather(city, unit):
    api_key = "cea48bdc21a9473299701605243010" 
    base_url = "http://api.weatherapi.com/v1/current.json"
    
    params = {
        "key": api_key,
        "q": city,
        "aqi": "no"
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        
        temperature = data["current"]["temp_f"] if unit == "Fahrenheit" else data["current"]["temp_c"]
        description = data["current"]["condition"]["text"].lower()
        icon = get_icon_path(description) 
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
    city = city_entry.get()
    unit = unit_var.get()
    if city:
        result = get_weather(city, unit)
        messagebox.showinfo("Weather", result)
    
        if icon_path:
            try:
                weather_icon = Image.open(icon_path)
                weather_icon = weather_icon.resize((50, 50), Image.ANTIALIAS)
                weather_image = ImageTk.PhotoImage(weather_icon)
                icon_label.config(image=weather_image)
                icon_label.image = weather_image
            except Exception as e:
                print("Error loading image:", e)
    else:
        messagebox.showwarning("Input Required", "Please enter a city name.")
    

    
root = tk.Tk()
root.title("Weather App")
root.geometry("300x300")

root.configure(bg="#87CEEB")

unit_var = tk.StringVar(value="Celcius")
unit_menu = tk.OptionMenu(root, unit_var, "Celsius", "Fahrenheit")
unit_menu.config(font=("Arial", 12))
unit_menu.pack(pady=5)

icon_label = tk.Label(root, bg="#87CEEB") 
icon_label.pack(pady=5)


city_entry = tk.Entry(root, width=20)
city_entry.pack(pady=10)

check_weather_button = tk.Button(root, text="Check Weather", command=show_weather)
check_weather_button.pack(pady=5)

print("Starting Tkinter mainloop...")
root.mainloop()


        