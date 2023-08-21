import tkinter as tk
from tkinter import ttk
from faker import Faker


class FakeDataGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Fake Data Generator")

        # Language selection
        self.label = tk.Label(self.master, text="Select a language:")
        self.label.pack(pady=10)

        self.languages = ['English', 'Italian', 'Hebrew', 'Japanese']
        self.lang_combo = ttk.Combobox(self.master, values=self.languages, state="readonly")
        self.lang_combo.current(0)
        self.lang_combo.pack(pady=10)

        # Button to generate data
        self.btn_generate = tk.Button(self.master, text="Generate Fake Data", command=self.get_fake_data)
        self.btn_generate.pack(pady=10)

        # Text box to display results
        self.output_text = tk.Text(self.master, width=50, height=10)
        self.output_text.pack(pady=10, padx=10)

    def generate_fake_data(self, language='en'):
        fake = Faker(language)

        if language == 'it':
            fake.locale = 'it_IT'
        elif language == 'he':
            fake.locale = 'he_IL'
        elif language == 'ja':
            fake.locale = 'ja_JP'
        else:
            fake.locale = 'en_US'

        fake_data = {
            'name': fake.name(),
            'address': fake.address(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
        }

        return fake_data

    def get_fake_data(self):
        lang = self.lang_combo.get().lower()
        if lang in ['english', 'italian', 'hebrew', 'japanese']:
            fake_data = self.generate_fake_data(lang[:2])
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Generated Fake Data:\n")
            for key, value in fake_data.items():
                self.output_text.insert(tk.END, f"{key.capitalize()}: {value}\n")
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Invalid language selection.")


class MainWindow(tk.Tk):
    font_large = ("Arial", 24)
    font_med = ("Arial", 12)
    font_small = ("Arial", 8)

    def __init__(self):
        super().__init__()
        self.ddosAttackBtn = None
        self.msspEncryptBtn = None
        self.vijnerEncAttack = None
        self.caesarEncAttack = None
        self.encStrBtn = None
        self.printSiteSrcBtn = None
        self.button_list = None
        self.fakeDataBtn = None
        self.title("HackerManTool")
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
        self.button_list.append((self.printSiteSrcBtn))
        self.encStrBtn = tk.Button(self, text="Encrypt string given hash function",
                                   font=self.font_med,
                                   command=self.onEncStrBtn)
        self.button_list.append(self.encStrBtn)
        self.caesarEncAttack = tk.Button(self, text="Attack on Caesar Code",
                                         font=self.font_med,
                                         command=self.onCaesarEncAttack)
        self.button_list.append(self.caesarEncAttack)
        self.vijnerEncAttack = tk.Button(self, text="Attack on Vijner Code",
                                         font=self.font_med,
                                         command=self.onVijnerEncAttack)
        self.button_list.append(self.vijnerEncAttack)
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

    def onFakeDataBtn(self):
        self.new_window_fd = tk.Toplevel(self)
        FakeDataGenerator(self.new_window_fd)

    def onPrintSiteSrcBtn(self):
        pass

    def onEncStrBtn(self):
        pass

    def onCaesarEncAttack(self):
        pass

    def onVijnerEncAttack(self):
        pass

    def onMsspEncryptBtn(self):
        pass

    def onDdosAttackBtn(self):
        pass


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
