from TwitchCubieBot import CubieBot
from TwitchCubieBot import View
from TwitchCubieBot import MessageSource
import json, time, logging, os, sys

from Log import Log
Log(__file__)

from Settings import Settings
from App import App

class AppView(View):
    def __init__(self, bot):
        super().__init__(bot)
    
    def output(self, message, source):
        
        if (source == MessageSource.AVERAGE_COMMAND_ERRORS and self.bot.average_command_errors) or \
            (source == MessageSource.AVERAGE_RESULTS and self.bot.average_results) or \
            (source == MessageSource.VOTING_COMMAND_ERRORS and self.bot.voting_command_errors) or \
            (source == MessageSource.VOTING_RESULTS and self.bot.voting_results):
            self.bot.app.add_message(message, enter=True)
        
        if (source == MessageSource.VOTES and self.bot.votes) or \
            (source == MessageSource.NUMBERS and self.bot.numbers):
            self.bot.app.add_message(message)

        super().output(message, source)

class Bot(CubieBot):
    def __init__(self):
        super().__init__()
        # Override the original View used in CubieBot with our custom AppView
        self.view = AppView(self)
        self.update_settings()
        # Override the Capabilities to also get subscription data
        self.capability = ["tags", "commands"]

    def update_settings(self):
        path = os.path.join(sys.path[0], "settings.txt")
        s = Settings(path)
        self.host, self.port, self.chan, self.nick, self.auth, self.denied_users, self.allowed_ranks, self.allowed_people, self.lookback_time, self.sub, \
            self.sub_gift_bomb, self.sub_gift, self.average_results, self.average_command_errors, self.voting_results, self.votes, self.voting_command_errors, self.numbers = s.get_settings()

    # Used from GUI
    def set_login_settings(self, host, port, chan, nick, auth):
        self.host = host
        self.port = port
        self.chan = chan
        self.nick = nick
        self.auth = auth
    
    # Used from GUI
    def set_user_settings(self, sub, sub_gift_bomb, sub_gift, average_results, average_command_errors, voting_results, votes, voting_command_errors, numbers):
        self.sub = sub
        self.sub_gift_bomb = sub_gift_bomb
        self.sub_gift = sub_gift
        self.average_results = average_results
        self.average_command_errors = average_command_errors
        self.voting_results = voting_results
        self.votes = votes
        self.voting_command_errors = voting_command_errors
        self.numbers = numbers

    # Man-in-the-middle between Twitch servers and the Bot, to display data in the GUI
    def message_handler(self, m):
        if m.type == "376":
            self.app.add_message("Successfully logged in as: {}.".format(self.nick), enter=True)

        elif m.type == "CAP * ACK":
            self.app.add_message("Successfully added requirement: {}.".format(", ".join(m.message.split("/")[1:])), enter=True)

        elif m.type == "366":
            self.app.add_message("Successfully joined: {}\nBot is active now.".format(self.chan), enter=True)

        elif m.type == 'USERNOTICE':
            # If someone Subscribes, Gift Bombs or Gift Subs, and the corresponding setting is set to true.
            if (m.tags["msg-id"] in ["subgift", "anonsubgift"] and self.sub_gift) or \
            (m.tags["msg-id"] in ["sub", "resub", "giftpaidupgrade", "anongiftpaidupgrade"] and self.sub) or \
            (m.tags["msg-id"] in ["submysterygift", "anonsubmysterygift"] and self.sub_gift_bomb):
                self.app.add_message(m.tags["system-msg"].replace("\\s", " "), True)

        elif m.type == "NOTICE":
            logging.info(m.message)
            self.app.add_message("Notice: " + m.message, True)
        
        super().message_handler(m)

if __name__ == "__main__":
    bot = Bot()
    app = App(bot)
    bot.app = app
