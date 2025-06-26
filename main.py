import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import requests
import os
from dotenv import load_dotenv

def get_moon_phase(api_key, date, location="Delhi"):
    city_coords = {
        "Delhi": (28.6139, 77.2090),
        "Mumbai": (19.0760, 72.8777),
        "Banglore": (12.9716, 77.5946),
        "New York": (40.7128, -74.0060),
        "Paris": (48.8566, 2.3522),
        "Tokyo": (35.6895, 139.6917),
        "London": (51.5074, -0.1278),
    }

    if location not in city_coords:
        print(f"Location '{location}' not supported. Using Delhi as default.")
        location = "Delhi"

    lat, long = city_coords[location]
    url = f"https://api.ipgeolocation.io/astronomy?apiKey={api_key}&lat={lat}&long={long}&date={date}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to get data:", response.status_code, response.text)
        return None

    data = response.json()
    return data

def show_data():
    date = date_entry.get()
    location = location_entry.get().strip() or "Delhi"

    data = get_moon_phase(api_key, date, location)
    if data:
        result = (
            f"Moonrise Time: {data.get('moonrise')}\n"
            f"Moonset Time: {data.get('moonset')}\n"
            f"Moon Phase: {data.get('moon_phase')}\n"
            f"Moon Illumination: {data.get('moon_illumination_percentage')}%\n"
        )
        result_label.config(text=result)

        phase = data.get('moon_phase')
        if phase:
            phase_cleaned = phase.strip().upper()
            print(f"DEBUG: API returned moon phase -> {phase_cleaned}")

            img_path = phase_to_image.get(phase_cleaned)
            if img_path and os.path.exists(img_path):
                moon_img_raw = Image.open(img_path)
                moon_img_raw = moon_img_raw.resize((200, 200))  
                moon_img = ImageTk.PhotoImage(moon_img_raw)
                image_label.config(image=moon_img)
                image_label.image = moon_img
            else:
                messagebox.showwarning("Image Not Found", f"No image found for phase: {phase_cleaned}")
                image_label.config(image="")  
        else:
            messagebox.showerror("Error", "Moon phase data is missing.")


# replace with your actual API key
load_dotenv()
api_key = os.getenv("MOON_API_KEY")

phase_to_image = {
    "FULL_MOON": "images/full_moon.jpg",
    "NEW_MOON": "images/new_moon.jpg",
    "WAXING_CRESCENT": "images/waxing_crescent.jpg",
    "WAXING_GIBBOUS": "images/waxing_gibbous.jpg",
    "WANING_CRESCENT": "images/waning_crescent.jpg",
    "WANING_GIBBOUS": "images/waning_gibbous.jpg",
    "FIRST_QUARTER": "images/first_quarter.jpg",
    "LAST_QUARTER": "images/last_quarter.jpg"
}

#window
root = tk.Tk()
root.title("Celestia")

title_label = tk.Label(root, text="Celestia", font=("Helvetica", 24, "bold"))
title_label.pack(pady=(10, 0)) 

subtitle_label = tk.Label(root, text="Find your Moon!", font=("Helvetica", 12, "italic"), fg="gray")
subtitle_label.pack(pady=(0, 15))  

tk.Label(root, text="Enter Date (YYYY-MM-DD):").pack()
date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
date_entry.pack()

tk.Label(root, text="Select or Type Location:").pack()

city_list = ["Delhi", "Mumbai", "Banglore", "New York", "Paris", "Tokyo", "London"]

location_entry = ttk.Combobox(root, values=city_list)
location_entry.current(0)   
location_entry.pack()

submit_btn = tk.Button(root, text="Get Moon Phase", command=show_data)
submit_btn.pack(pady=10)

result_label = tk.Label(root, text="", justify="left")
result_label.pack()

image_label = tk.Label(root)
image_label.pack(pady=10)

#run
root.mainloop()


