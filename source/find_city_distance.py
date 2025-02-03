# Calculating city distance using longitude and latitude
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json

class FindDistance:
    def __init__(self, root):
        self.root = root
        self.root.title("Find City Distance")
        
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.entry_filename = tk.Entry(self.frame, width=40)
        self.entry_filename.pack(side=tk.LEFT, padx=5)

        self.browse_button = tk.Button(self.frame, text="Browse", command=self.browse_json_file)
        self.browse_button.pack(side=tk.LEFT, padx=(5, 10))

        self.read_button = tk.Button(self.frame, text="Calculate Distance", command=self.calculate_city_distance)
        self.read_button.pack(side=tk.TOP, padx=(5, 10))

    def browse_json_file(self):
        self.file_path = filedialog.askopenfilename(title="Select a JSON file",
                                                    filetypes=[("JSON files", "*.json")])
        print("browse_json_file")

    def calculate_city_distance(self):
        print("calculate_city_distance")


if __name__ == "__main__":
    root = tk.Tk()
    app = FindDistance(root)
    root.mainloop()