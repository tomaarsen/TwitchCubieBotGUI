
import logging

from TwitchWebsocket.Message import Message

from Settings import Settings
from Log import Log
Log(__file__)

# Modules
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.font as tkFont
import time, json, os, sys, threading
from datetime import datetime
from functools import reduce

class App(threading.Thread):

    # Initialise the thread
    def __init__(self, bot):
        threading.Thread.__init__(self)
        
        # Attributes
        self.bot = bot
        self.settings_open = False

        # Start the thread
        self.start()

    # Quit properly
    def callback(self):
        # Quit the GUI
        self.root.quit()
        # Join the bot thread
        self.bot.stop()
        # This terminates the entire program

    # Clear output field
    def clear(self):
        self.txt.delete("1.0", tk.END)

    # Hide the OAUTH password
    def hide(self):
        if self.login_entries[4]['state'] == 'normal':
            self.oauth = self.login_entries[4].get()
            self.login_entries[4].delete(0, tk.END)
            self.login_entries[4].insert(0, "*" * 44)
            self.login_entries[4].configure(state='readonly')
        else:
            self.login_entries[4].configure(state='normal')
            self.login_entries[4].delete(0, tk.END)
            self.login_entries[4].insert(0, self.oauth)
    
    # Settings popup page
    def settings(self):
        # Prevent another popup from opening if one is already open
        if self.settings_open:
            return

        self.settings_open = True

        # Set up popup
        self.popup = tk.Toplevel()
        self.popup.wm_title("Settings")
        self.popup.minsize(width=165, height=238)
        self.popup.protocol("WM_DELETE_WINDOW", self.save_settings)

        lbl = tk.Label(self.popup, text="Developed by CubieDev")
        lbl.grid(column=0, columnspan=2)

        # Variables
        entries = ['Sub', 'Sub Gift Bomb', 'Sub Gift', 'Average Results', 'Average Cmd Errors', 'Vote Results', 'Votes', 'Vote Cmd Errors', 'Numbers']
        settingsName = [self.bot.sub, self.bot.sub_gift_bomb, self.bot.sub_gift, self.bot.average_results, self.bot.average_command_errors, self.bot.voting_results, self.bot.votes, self.bot.voting_command_errors, self.bot.numbers]
        self.settings_entries = []

        # Create all checkbox buttons
        for x, e in enumerate(entries):
            # Readonly Text Field for setting names
            entry = tk.Entry(self.popup, borderwidth=1)
            entry.grid(sticky="W", padx=(8, 0), pady=(0, 4))
            entry.insert(0, e)
            entry.configure(state='readonly')

            # Checkboxes
            v = tk.IntVar()
            v.set(settingsName[x])
            w = tk.Checkbutton(self.popup, relief="sunken", borderwidth=1, variable=v)
            w.grid(row=x+1, column=1)
            self.settings_entries.append(v)
        
        btn = tk.Button(self.popup, text="Save & Close", width=20, command=self.save_settings)
        btn.grid(columnspan=2, sticky="NEWS", padx=(6, 0), pady=(4, 6))

    def update_login(self):
        # Get settings
        login = [entry.get() for entry in self.login_entries]
        # Set the settings on the bot
        chan = login[2] if len(login[2]) > 0 and login[2][0] == "#" else "#" + login[2]
        try:
            port = int(login[1])
        except:
            port = 0
        if self.login_entries[4]['state'] == 'normal':
            auth = login[4]
        else:
            auth = self.oauth

        self.bot.set_login_settings(login[0], port, chan, login[3], auth)

    # Save the settings to a file
    def save_settings(self):
        # Get settings
        settings = [entry.get() for entry in self.settings_entries]
        # Set the settings on the bot
        self.bot.set_user_settings(settings[0], settings[1], settings[2], settings[3], settings[4], settings[5], settings[6], settings[7], settings[8])
        # Update the file
        path = os.path.join(sys.path[0], "settings.txt")
        Settings.update(path, self.bot)
        # Make sure this popup can be opened again later
        self.settings_open = False
        # And remove the popup
        self.popup.destroy()

    # Vote button functionality
    def vote(self):
        # Vote with text
        self.bot.command_vote(Message(":cubiedev!cubiedev@cubiedev.tmi.twitch.tv PRIVMSG #cubiedev :!vote"))

    def run(self):
        self.login_dict = {"Host": self.bot.host, "Port":self.bot.port, "Chan": self.bot.chan.replace("#", ""), "User": self.bot.nick, "Auth": self.bot.auth}

        # Set up GUI
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.resizable(0, 1)
        self.root.minsize(width=283, height=205)
        self.root.title("Twitch Bot GUI")
        self.root.grid_rowconfigure(6, weight=1)
        
        self.login_entries = []
        self.oauth = ""
        
        # Handle Run/Stop button functionality
        def run_stop():
            if self.run_stop_button['text'] == "Run":
                self.update_login()
                self.bot.start()
            else:
                self.bot.stop()
                self.add_message("Bot has been stopped.", True)
            self.run_stop_button.configure(text=["Stop", "Run"][self.run_stop_button['text'] == "Stop"])

        self.m = max([len(str(self.login_dict[i])) for i in self.login_dict]) + 1

        # Fields for the GUI main page
        for x, i in enumerate(self.login_dict):
            if x == 4:
                self.hide_button = tk.Button(self.root, text=i, command=self.hide)
                self.hide_button.grid(row=x, padx=(12, 4))
                self.hide_button.config(width=4)
            else:
                tk.Label(self.root, text=i + ":").grid(row=x, padx=(12, 4))
            e = tk.Entry(self.root, width=self.m)
            e.grid(row=x, column=1, sticky="W", columnspan=5, pady=2)
            e.insert(0, self.login_dict[i])
            self.login_entries.append(e)
        
        # Hide the OAUTH password.
        self.hide()

        # Run/Stop Button
        self.run_stop_button = tk.Button(self.root, text='Run', command=run_stop)
        self.run_stop_button.grid(row=len(self.login_dict), column=0, pady=4, padx=(9, 0))
        self.run_stop_button.config(width=4)

        # Clear, Vote and Settings buttons
        tk.Button(self.root, text='Clear', command=self.clear).grid(row=len(self.login_dict), column=1, pady=4)
        tk.Button(self.root, text='Vote', command=self.vote).grid(row=len(self.login_dict), column=3, pady=4, padx=(4, 0))
        tk.Button(self.root, text='Settings', command=self.settings).grid(row=len(self.login_dict), column=5, pady=4, padx=(74, 25))

        # Output field
        self.txt = tkst.ScrolledText(self.root, undo=True, borderwidth=3, relief="groove", width=self.m, height=17)
        self.txt.config(font=('consolas', '8'), undo=True, wrap='word') #font=('consolas', '12')
        self.txt.grid(column=0, padx=(10, 6), pady=(2, 5), sticky="news", columnspan=6)

        # Configure bold font for specific output messages to use
        self.bold_font = tkFont.Font(self.txt, self.txt.cget("font"))
        self.bold_font.configure(weight="bold")
        self.txt.tag_configure("bold", font=self.bold_font)

        # GUI Loop
        self.root.mainloop()

    # Add message to the output field
    def add_message(self, message, enter=False):
        ending = self.get_message()
        message = str(message)
        m = ", " + message
        if enter:
            if ending == "\n\n" or ending == "\n":
                m = message + "\n"
            else:
                m = "\n" + message + "\n"
        elif ending == "\n\n" or ending == "\n":
            m = message
        if enter:
            self.txt.insert(tk.END, m, "bold")
        else:
            self.txt.insert(tk.END, m)
        if self.txt.yview()[1] > 0.90:
            self.txt.see(tk.END)

    # Get last two characters from the output field
    def get_message(self):
        return self.txt.get(1.0, tk.END)[-2:]
