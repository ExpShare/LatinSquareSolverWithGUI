import customtkinter


class Cell:
    def __init__(self, value, row, column):
        self.value = value
        self.row = int(row)
        self.column = int(column)

    def getValue(self):
        return self.value

    def getRow(self):
        return self.row

    def getCol(self):
        return self.column

    def setValue(self, value):
        self.value = value


class MyPlayingFieldBoxFrame(customtkinter.CTkFrame):
    def __init__(self, master, button_command):
        super().__init__(master)

        self.buttons = []

        '''
        parameters for buttons 2x2 grid
        "Name on button-- | row | column | value--(on start)
        '''
        playing_field_buttons = [
            ("Button 11", 0, 0, 0),
            ("Button 12", 0, 1, 0),
            ("Button 21", 1, 0, 0),
            ("Button 22", 1, 1, 0),
        ]

        for text, row, col, value in playing_field_buttons:
            cell = Cell(value, row, col)

            button = customtkinter.CTkButton(self, text=text)
            button.cell = cell   # attach the Cell object to the button!!!

            button.configure(command=lambda b=button: button_command(b))
            button.grid(row=row, column=col, padx=5, pady=5)

            self.buttons.append(button)


class ActionButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master, action_command):
        super().__init__(master)

        action_buttons = [
            ("A", "#FF0909", "A", 0, 0, 1),
            ("B", "#2804F5", "B", 0, 1, 2),
            ("C", "#44F504", "C", 0, 2, 3),
            ("D", "#F5E904", "D", 0, 3, 4),
        ]

        for text, color, new_button_text, row, col, value in action_buttons:
            button = customtkinter.CTkButton(
                self,
                text=text,
                command=lambda c=color, n=new_button_text, v=value: action_command(c, n, v)
            )
            button.grid(row=row, column=col, padx=5, pady=5)


class SolveFrame(customtkinter.CTkFrame):
    def __init__(self, master, solve_command):
        super().__init__(master)

        solveButton = customtkinter.CTkButton(self, text="Solve", command=solve_command)
        solveButton.grid(row=0, column=0, padx=5, pady=5)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # "Set-up on start" kind od but the buttons have actions that can change their state
        self.title("my app")
        self.geometry("500x300")

        self.selected_color = None
        self.selected_name = None
        self.selected_value = 0

        # Don't know what this does
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.playing_field_frame = MyPlayingFieldBoxFrame(self, self.paint_button_and_change_name)
        self.playing_field_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # If I go over to my action frame and click, then we execute the function connected with this type of button.
        self.action_frame = ActionButtonFrame(self, self.select_color_and_name)
        self.action_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.solve_frame = SolveFrame(self, self.saveSolution)
        self.solve_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    def select_color_and_name(self, color, name, value):
        self.selected_color = color
        self.selected_name = name
        self.selected_value = value

    def paint_button_and_change_name(self, button):
        if self.selected_color is not None:
            button.configure(fg_color=self.selected_color)

        if self.selected_name is not None:
            button.configure(text=self.selected_name)

        # update the Cell object too
        button.cell.setValue(self.selected_value)

    # we force a nxn matrix and print it.
    def saveSolution(self):
        buttons = self.playing_field_frame.buttons

        max_row = max(button.cell.getRow() for button in buttons)
        max_col = max(button.cell.getCol() for button in buttons)

        n = max(max_row + 1, max_col + 1)

        matrix = [[0 for _ in range(n)] for _ in range(n)]

        for button in buttons:
            cell = button.cell
            matrix[cell.getRow()][cell.getCol()] = cell.getValue()

        print(matrix)


app = App()
app.mainloop()
