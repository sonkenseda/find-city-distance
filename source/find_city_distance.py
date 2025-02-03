# Calculating city distance using longitude and latitude
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json

class FindDistance:
    def __init__(self, root, json_output):
        self.root = root
        self.json_output = json_output
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
        print("calculate_city_distance")
        with open(self.master_file_path, 'r') as master_file:
            master_data = json.load(master_file)

        city_code_lookup = {entry['city_code']: entry for entry in master_data}
        airport_code_lookup = {entry['code']: entry for entry in master_data}

        with open(self.json_output, 'w') as output_file:
            output_file.write('[')  # Start the JSON array
            first = True  # Flag to ensure proper comma placement between objects

            # Open user data
            with open(self.city_file_path, 'r') as city_file:
                data = json.load(city_file)
                for obj in data:
                    origin_code = obj['origin_airport']
                    destination_code = obj['destination_airport']

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

                    # Write the updated entry to the output file
                    if not first:
                        output_file.write(',\n')
                    output_file.write(json.dumps(obj, indent=4))
                    first = False

            output_file.write('\n]')  # End the JSON array



if __name__ == "__main__":
    json_output = "calculated_distance.json"
    root = tk.Tk()
    app = FindDistance(root, json_output)
    root.mainloop()