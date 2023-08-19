import tkinter as tk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HackerManTool")

        self.create_widgets()
        self.configure_grid()

    def create_buttons(self):
        btn_font = ("Arial", 12)
        button_list = []
        self.fakeDataBtn = tk.Button(self, text="Create Random Fake Data",
                                     font=btn_font,
                                     command=self.onFakeDataBtn)
        button_list.append(self.fakeDataBtn)
        self.printSiteSrcBtn = tk.Button(self, text="Print Site Source Code and Button Locations",
                                         font=btn_font,
                                         command=self.onPrintSiteSrcBtn)
        button_list.append((self.printSiteSrcBtn))
        self.encStrBtn = tk.Button(self, text="Encrypt string given hash function",
                                   font=btn_font,
                                   command=self.onEncStrBtn)
        button_list.append(self.encStrBtn)
        self.caesarEncAttack = tk.Button(self, text="Attack on Caesar Code",
                                         font=btn_font,
                                         command=self.onCaesarEncAttack)
        button_list.append(self.caesarEncAttack)
        self.vijnerEncAttack = tk.Button(self, text="Attack on Vijner Code",
                                         font=btn_font,
                                         command=self.onVijnerEncAttack)
        button_list.append(self.vijnerEncAttack)


    def create_widgets(self):
        # Add a label at the top with the program name
        title_label = tk.Label(self, text="HackerManTool", font=("Arial", 24))
        title_label.grid(row=0, column=0, columnspan=1, pady=20)  # centered at the top of the window

        # Define button positions for the first 6 buttons
        button_positions = [
            (1, 0), (1, 1), (1, 2),  # Row 1
            (2, 0), (2, 1), (2, 2)  # Row 2
        ]

        for i, (r, c) in enumerate(button_positions):
            btn = tk.Button(self, text=f"Button {i + 1}")
            btn.grid(row=r, column=c, padx=10, pady=10, sticky="ew")

        # The 7th button is centered and takes the full grid width
        btn7 = tk.Button(self, text="Button 7")
        btn7.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    def configure_grid(self):
        # Configure the rows
        self.grid_rowconfigure(0, weight=0)  # Header label
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Configure the columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def onFakeDataBtn(self):
        pass

    def onPrintSiteSrcBtn(self):
        pass

    def onEncStrBtn(self):
        pass

    def onCaesarEncAttack(self):
        pass

    def onVijnerEncAttack(self):
        pass


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
