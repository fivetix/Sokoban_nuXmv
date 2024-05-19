import tkinter as tk

class SokobanBoard:
    def __init__(self, master):
        self.master = master
        self.tiles = {}  # Dictionary to store the tile types

        # Interface for changing dimensions
        self.row_entry = tk.Entry(master, width=5)
        self.row_entry.grid(row=0, column=1)
        self.col_entry = tk.Entry(master, width=5)
        self.col_entry.grid(row=0, column=3)
        tk.Label(master, text="Rows:").grid(row=0, column=0)
        tk.Label(master, text="Cols:").grid(row=0, column=2)
        tk.Button(master, text='Rebuild Board', command=self.rebuild_board).grid(row=0, column=4)
        tk.Button(master, text='Print Board', command=self.print_board).grid(row=0, column=5)

        self.board_frame = tk.Frame(master)
        self.board_frame.grid(row=1, columnspan=6)

        self.default_rows = 5
        self.default_cols = 5
        self.rebuild_board(self.default_rows, self.default_cols)

    def rebuild_board(self, rows=None, cols=None):
        rows = int(self.row_entry.get()) if self.row_entry.get() else self.default_rows
        cols = int(self.col_entry.get()) if self.col_entry.get() else self.default_cols
        self.row_entry.delete(0, tk.END)
        self.row_entry.insert(0, str(rows))
        self.col_entry.delete(0, tk.END)
        self.col_entry.insert(0, str(cols))

        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.tiles = {}
        for row in range(rows):
            for col in range(cols):
                button = tk.Button(self.board_frame, text='-', width=4, height=2,
                                   command=lambda r=row, c=col: self.on_click(r, c))
                button.grid(row=row, column=col)
                self.tiles[(row, col)] = button

    def on_click(self, row, col):
        current_text = self.tiles[(row, col)]['text']
        next_text = {'-': '#', '#': '$', '$': '.', '.': '@', '@': '+','+':
        '*','*':'-'}
        new_text = next_text[current_text]
        self.tiles[(row, col)]['text'] = new_text

    def print_board(self):
        board = []
        rows = int(self.row_entry.get())
        cols = int(self.col_entry.get())
        for row in range(rows):
            current_row = ''
            for col in range(cols):
                current_row += self.tiles[(row, col)]['text']
            board.append(current_row)
        print('\n'.join(board))

root = tk.Tk()
SokobanBoard(root)
root.mainloop()
