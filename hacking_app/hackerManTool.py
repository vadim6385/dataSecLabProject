import hashlib
import tkinter as tk
from tkinter import ttk, scrolledtext

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


class MainWindow(tk.Tk):
    font_large = ("Arial", 24)
    font_med = ("Arial", 12)
    font_small = ("Arial", 8)

    def __init__(self):
        super().__init__()
        self.new_window_fd = None
        self.ddosAttackBtn = None
        self.msspEncryptBtn = None
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
        self.font_med = ("Arial", 12)
        self.button_list = []
        self.fakeDataBtn = tk.Button(self, text="Create Random Fake Data",
                                     font=self.font_med,
                                     command=self.onFakeDataBtn)
        self.button_list.append(self.fakeDataBtn)
        self.printSiteSrcBtn = tk.Button(self, text="Print Site Source Code and Button Locations",
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
        self.msspEncryptBtn = tk.Button(self, text="MSSP Encryption",
                                        font=self.font_med,
                                        command=self.onMsspEncryptBtn)
        self.button_list.append(self.msspEncryptBtn)
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
        pass

    def onEncStrBtn(self):
        self._open_window("Encrypt String", EncryptionAppGUI)

    def onCaesarEncAttack(self):
        self._open_window("Caesar", CaesarCipherGUI)

    def onVigenereEncAttack(self):
        self._open_window("Vigenere", VigenereCipherGUI)

    def onMsspEncryptBtn(self):
        pass

    def onDdosAttackBtn(self):
        pass


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
