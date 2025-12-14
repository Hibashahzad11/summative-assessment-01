import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO


class CountryAPI:
    """Handles all communication with the REST Countries API"""

    def get_country(self, name):
        # Build API URL using the country name
        url = f"https://restcountries.com/v3.1/name/{name}"

        # Send GET request to the API
        response = requests.get(url)

        # If request fails, return None
        if response.status_code != 200:
            return None

        # Return the first matching country result
        return response.json()[0]


class CountryApp:
    """Main GUI application for displaying country information"""

    def __init__(self, root):
        # Configure main window
        self.root = root
        self.root.title("Rest Countries Explorer")
        self.root.geometry("550x500")
        self.root.configure(bg="#212121")

        # Initialize API handler and flag image reference
        self.api = CountryAPI()
        self.flag_image = None

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Application title
        tk.Label(
            self.root,
            text="🌍 Rest Countries Explorer",
            font=("Century", 24, "bold"),
            bg="#212121",
            fg="white"
        ).pack(pady=15)

        # Frame to hold input widgets
        input_frame = tk.Frame(self.root, bg="#212121")
        input_frame.pack(pady=10)

        # Label for country input
        tk.Label(
            input_frame,
            text="Country Name:",
            font=("Century", 14, "bold"),
            bg="#212121",
            fg="white"
        ).grid(row=0, column=0, padx=5)

        # Entry field for user input
        self.country_entry = tk.Entry(
            input_frame,
            font=("Century", 14),
            width=25,
            bg="#161616",
            fg="white",
            insertbackground="white"
        )
        self.country_entry.grid(row=0, column=1, padx=5)

        # Button to search for country data
        tk.Button(
            input_frame,
            text="Search",
            font=("Century", 12, "bold"),
            command=self.search_country
        ).grid(row=0, column=2, padx=5)

        # Button to clear input and results
        tk.Button(
            input_frame,
            text="Clear",
            font=("Century", 12, "bold"),
            command=self.clear_all
        ).grid(row=0, column=3, padx=5)

        # Frame to display country information
        self.result_frame = tk.Frame(self.root, bg="#161616")
        self.result_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Label to show country details
        self.result_label = tk.Label(
            self.result_frame,
            font=("Century", 13),
            bg="#161616",
            fg="white",
            justify="left",
            anchor="nw"
        )
        self.result_label.pack(padx=10, pady=10, fill="both", expand=True)

        # Label to display the country flag
        self.flag_label = tk.Label(self.result_frame, bg="#161616")
        self.flag_label.pack(pady=5)

    def search_country(self):
        # Get user input and remove extra spaces
        country_name = self.country_entry.get().strip()

        # Validate input
        if not country_name:
            messagebox.showwarning("Input Error", "Please enter a country name.")
            return

        # Fetch country data from API
        data = self.api.get_country(country_name)

        # Handle invalid country names
        if data is None:
            messagebox.showerror("Error", "Country not found.")
            self.clear_all()
            return

        # Display fetched country data
        self.display_country(data)

    def display_country(self, data):
        # Extract relevant information from API response
        name = data.get("name", {}).get("common", "N/A")
        capital = data.get("capital", ["N/A"])[0]
        region = data.get("region", "N/A")
        population = data.get("population", 0)
        area = data.get("area", "N/A")
        flag_url = data.get("flags", {}).get("png", "")

        # Display formatted country information
        self.result_label.config(
            text=(
                f"Country: {name}\n\n"
                f"Capital: {capital}\n"
                f"Region: {region}\n"
                f"Population: {population:,}\n"
                f"Area: {area} km²"
            )
        )

        # Download and display the country flag
        if flag_url:
            image_data = requests.get(flag_url).content
            image = Image.open(BytesIO(image_data)).resize((120, 80))
            self.flag_image = ImageTk.PhotoImage(image)
            self.flag_label.config(image=self.flag_image)

    def clear_all(self):
        # Clear input field and displayed results
        self.country_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.flag_label.config(image="")


# Program entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = CountryApp(root)
    root.mainloop()
