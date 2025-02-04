# Calculating city distance using longitude and latitude
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import csv
import json
import math

class FindDistance:
    def __init__(self, root, json_output, csv_output):
        self.root = root
        self.json_output = json_output
        self.csv_output = csv_output
        self.root.title("Find City Distance")
        
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Frame for the first entry (master CSV) and browse button
        self.entry_frame1 = tk.Frame(self.frame)
        self.entry_frame1.pack(side=tk.TOP, pady=5)

        self.entry_master_csv = tk.Entry(self.entry_frame1, width=40)
        self.entry_master_csv.pack(side=tk.LEFT, padx=5)

        self.browse_button1 = tk.Button(self.entry_frame1, text="Browse", command=self.browse_master_json_file)
        self.browse_button1.pack(side=tk.LEFT, padx=5)

        # Frame for the second entry (city CSV) and browse button
        self.entry_frame2 = tk.Frame(self.frame)
        self.entry_frame2.pack(side=tk.TOP, pady=5)

        self.entry_city_csv = tk.Entry(self.entry_frame2, width=40)
        self.entry_city_csv.pack(side=tk.LEFT, padx=5)

        self.browse_button2 = tk.Button(self.entry_frame2, text="Browse", command=self.browse_city_json_file)
        self.browse_button2.pack(side=tk.LEFT, padx=5)

        # Frame for buttons
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(side=tk.TOP, pady=10)

        # Read button
        self.read_button = tk.Button(self.button_frame, text="Calculate Distance", command=self.calculate_city_distance)
        self.read_button.pack(side=tk.TOP, padx=(5, 10), pady=5)


    def browse_master_json_file(self):
        self.master_file_path = filedialog.askopenfilename(title="Select a JSON file",
                                                    filetypes=[("JSON files", "*.json")])
        if self.master_file_path:
            self.entry_master_csv.delete(0, tk.END)
            self.entry_master_csv.insert(0, self.master_file_path)

    def browse_city_json_file(self):
        self.city_file_path = filedialog.askopenfilename(title="Select a JSON file",
                                                    filetypes=[("JSON files", "*.json")])
        if self.city_file_path:
            self.entry_city_csv.delete(0, tk.END)
            self.entry_city_csv.insert(0, self.city_file_path)

    def calculate_city_distance(self):
        to_json_data = []
        with open(self.master_file_path, 'r') as master_file:
            master_data = json.load(master_file)

        city_code_lookup = {entry['city_code']: entry for entry in master_data}
        airport_code_lookup = {entry['code']: entry for entry in master_data}

        # Open user data
        with open(self.city_file_path, 'r') as city_file:
            data = json.load(city_file)
            for obj in data:
                origin_code = obj['origin_city']
                destination_code = obj['destination_city']

                # Lookup origin and destination city info from city_code (fallback to airport_code)
                origin_info = city_code_lookup.get(origin_code) or airport_code_lookup.get(origin_code)
                destination_info = city_code_lookup.get(destination_code) or airport_code_lookup.get(destination_code)

                # Add latitude and longitude if found
                if origin_info:
                    obj['origin_latitude'] = origin_info['latitude']
                    obj['origin_longitude'] = origin_info['longitude']
                if destination_info:
                    obj['destination_latitude'] = destination_info['latitude']
                    obj['destination_longitude'] = destination_info['longitude']
                
                self.origin_latitude = obj['origin_latitude']
                self.origin_longitude = obj['origin_longitude']
                self.destination_latitude = obj['destination_latitude']
                self.destination_longitude = obj['destination_longitude']

                obj['distance_kms'] = self.haversine_formula()
                to_json_data.append(obj)

        with open(self.json_output, 'w') as output_file:
            output_file.write(json.dumps(to_json_data, indent=4))

        self.export_to_csv()
        messagebox.showinfo("Success", f"JSON file has been created: {self.csv_output}")
        self.root.quit()

    @staticmethod
    def deg_to_rad(deg):
        return deg * (math.pi / 180)

    def haversine_formula(self):
        # Radius of Earth in km
        earth_rad = 6371.0

        # Converting longitude and latitude to radians
        origin_lat = self.deg_to_rad(float(self.origin_latitude))
        origin_long = self.deg_to_rad(float(self.origin_longitude))
        destination_lat = self.deg_to_rad(float(self.destination_latitude))
        destination_long = self.deg_to_rad(float(self.destination_longitude))

        # Get the difference between coordinates
        latitude_diff = destination_lat - origin_lat
        longitude_diff = destination_long - origin_long

        # Computation
        a = math.sin(latitude_diff / 2) ** 2 + math.cos(origin_lat) * math.cos(destination_lat) * math.sin(longitude_diff / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Distance in km
        self.distance = earth_rad * c
        return str(self.distance)
    
    def export_to_csv(self):
        print("export_to_csv")
        with open(self.json_output, 'r') as json_file:
            data = json.load(json_file)

        with open(self.csv_output, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            writer.writeheader()  # Write the header (fieldnames)
            writer.writerows(data)  # Write the rows

if __name__ == "__main__":
    json_output = "output/calculated_distance_YYYYMMDD.json"
    csv_output = "output/output_YYYYMMDD.csv"
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y%m%d')

    json_output = json_output.replace('YYYYMMDD', formatted_date)
    csv_output = csv_output.replace('YYYYMMDD', formatted_date)
    root = tk.Tk()
    app = FindDistance(root, json_output, csv_output)
    root.mainloop()