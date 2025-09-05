import tkinter as tk
import random
class matchGame:
    def __init__(self,root):
        self.root = root
        self.root.title("matchGame")
        self.cards = []
        self.buttons = []
        self.lock = False
        self.flipped = []
        self.matched = [False for i in range(40)]
        self.matchCount = 0
        self.finish_label = tk.Label(self.root, text ="Remember The Cards")
        self.finish_label.grid(row = 5, column = 0, columnspan = 10, pady = 10)
        self.start()
    def start(self):
        self.cards = [f'{i}' for i in range(1,21)] * 2
        random.shuffle(self.cards)
        self.create_board()
        self.root.after(10000, self.hide_cards)
    def create_board(self):
        for i, card in enumerate(self.cards):
            btn = tk.Button(self.root,text = card, width = 6, height = 3,command = lambda idx = i : self.flip(idx))
            btn.grid(row = i // 10, column = i % 10, padx = 5, pady = 5)
            self.buttons.append(btn)
    def hide_cards(self):
        for btn in self.buttons:
            btn.config(text="")
    def flip(self, idx):
        if self.lock or idx in self.flipped or self.matched[idx]:
            return
        self.buttons[idx].config(text = self.cards[idx])
        self.flipped.append(idx)
        if len(self.flipped) == 2:
            self.lock = True
            self.root.after(1000,self.check_match)

    def check_match(self):
        if(self.cards[self.flipped[0]] == self.cards[self.flipped[1]]):
            self.matched[self.flipped[0]] = True
            self.matched[self.flipped[1]] = True
            self.matchCount += 1
        else:
            self.buttons[self.flipped[0]].config(text = "")
            self.buttons[self.flipped[1]].config(text = "")
        self.flipped.clear()
        self.lock = False
        if(self.matchCount == 20):
            self.finish_label.config(text="Congratulations!")
if __name__ == "__main__":
    root = tk.Tk()
    game = matchGame(root)
    #window at mid
    window_width = root.winfo_screenwidth()    
    window_height = root.winfo_screenheight()  

    width = 630
    height = 295
    left = int((window_width - width)/2)       
    top = int((window_height - height)/2)      
    root.geometry(f'{width}x{height}+{left}+{top}')
    root.mainloop()
