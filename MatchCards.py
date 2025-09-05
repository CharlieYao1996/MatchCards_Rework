import tkinter as tk
from PIL import Image, ImageTk
import random, os
class MatchGame:
    def __init__(self,root):
        self.root = root
        self.root.title("Match Game")
        #Load card images
        self.images = {}
        self.back_img = None
        self.load_images()
        #game state
        self.cards = []
        self.buttons = []
        self.lock = True
        self.flipped = []
        self.matched = [False for i in range(40)]
        self.matchCount = 0
        #Record
        self.attempts = 0
        self.time_elapset = 0
        self.timer_running = False
        self.best_time = None
        self.best_attempts = None
        #labels
        self.status_label = tk.Label(self.root, text = "Time : 0s | Attempts : 0")
        self.status_label.grid(row = 5, column = 0, columnspan = 10, pady = 10)
        self.finish_label = tk.Label(self.root, text = "Remember The Cards")
        self.finish_label.grid(row = 6, column = 0, columnspan = 10, pady = 10)
        self.best_label = tk.Label(self.root, text ="")
        self.best_label.grid(row = 7, column = 0, columnspan = 10, pady = 10)
        #Restart buttons
        self.restart_button = tk.Button(self.root, text = "Restart Game",command = self.reset_game)
        self.restart_button.grid(row = 8, column = 0, columnspan = 10, pady = 10)
        #Game start
        self.prepare()
    def load_images(self):
        '''load cards image'''
        for card in [f'{i}' for i in range(1,21)]:
            path = os.path.join("images",f"{card}.png")
            img = Image.open(path).resize((60,90))
            self.images[card] = ImageTk.PhotoImage(img)
        back_path = os.path.join("images", "back.png")
        self.back_img = ImageTk.PhotoImage(Image.open(back_path).resize((60, 90)))
    def prepare(self):
        '''shuffle and wait 10 second to show the cards'''
        self.cards = [f'{i}' for i in range(1,21)] * 2
        random.shuffle(self.cards)
        self.create_board()
        self.root.after(10000, self.start)
    def create_board(self):
        '''create the button and show cards'''
        for i, card in enumerate(self.cards):
            btn = tk.Button(self.root, image = self.images[self.cards[i]],command = lambda idx = i : self.flip(idx))
            btn.grid(row = i // 10, column = i % 10, padx = 5, pady = 5)
            self.buttons.append(btn)
    def start(self):
        '''get ready to start'''
        self.hide_cards()
        self.finish_label.config(text = "")
        self.lock = False
        self.timer_running = True
        self.update_timer()        
    def hide_cards(self):
        '''hide all cards'''
        for btn in self.buttons:
            btn.config(image=self.back_img)
    def update_timer(self):
        '''update timer every second'''
        if self.timer_running:
            self.time_elapset += 1
            self.status_label.config(text = f"Time : {self.time_elapset}s | Attempts : {self.attempts}")
            self.root.after(1000,self.update_timer)
    def flip(self, idx):
        '''handle card flip'''
        if self.lock or idx in self.flipped or self.matched[idx]:
            return
        self.buttons[idx].config(image = self.images[self.cards[idx]])
        self.flipped.append(idx)
        if len(self.flipped) == 2:
            self.lock = True
            self.attempts += 1
            self.root.after(1000,self.check_match)

    def check_match(self):
        '''check if two flipped cards matched or not and check end'''
        if(self.cards[self.flipped[0]] == self.cards[self.flipped[1]]):
            self.matched[self.flipped[0]] = True
            self.matched[self.flipped[1]] = True
            self.matchCount += 1
        else:
            self.buttons[self.flipped[0]].config(image=self.back_img)
            self.buttons[self.flipped[1]].config(image=self.back_img)
        self.flipped.clear()
        self.lock = False
        if(self.matchCount == 20):
            self.timer_running = False
            if self.best_time is None or self.time_elapset < self.best_time:
                self.best_time = self.time_elapset
                self.best_attempts = self.attempts
            if self.time_elapset == self.best_time and self.attempts < self.best_attempts:
                self.best_attempts = self.attempts
            self.status_label.config(text=f"Finished Time : {self.time_elapset}s | Attempts : {self.attempts}")
            self.best_label.config(text=f"Best Time : {self.best_time}s | Attempts : {self.best_attempts}")
            self.finish_label.config(text="Congratulations!")
    def reset_game(self):
        '''reset the game and go prepare'''
        self.buttons = []
        self.lock = True
        self.flipped.clear()
        self.matched = [False for i in range(40)]
        self.matchCount = 0
        self.attempts = 0
        self.time_elapset = 0
        self.timer_running = False
        self.status_label.config(text = "Time : 0s | Attempts : 0")
        self.finish_label.config(text = "Remember The Cards")
        self.prepare()
if __name__ == "__main__":
    root = tk.Tk()
    game = MatchGame(root)
    #window at mid
    window_width = root.winfo_screenwidth()    
    window_height = root.winfo_screenheight()  

    width = 775
    height = 600
    left = int((window_width - width)/2)       
    top = int((window_height - height)/2)      
    root.geometry(f'{width}x{height}+{left}+{top}')
    root.mainloop()
