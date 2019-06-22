from TwitchWebsocket import TwitchWebsocket
import json, time, logging, os

from Log import Log
Log(__file__)

from Settings import Settings
from App import App

class Messages:
    # Message class to store information about a message.
    def __init__(self, sender, message):
        self.sender = sender
        self.message = message
        self.timestamp = round(time.time())

class CubieBot:
    def __init__(self):
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.capability = "tags"
        self.denied_users = None
        self.allowed_ranks = None
        self.allowed_people = None
        self.messages = {"Txt": {}, "Nr": {}}
        self.sub = None
        self.sub_gift_bomb = None
        self.sub_gift = None
        self.average_results = None
        self.average_command_errors = None
        self.voting_results = None
        self.votes = None
        self.voting_command_errors = None
        self.numbers = None
        self.app = None
        
        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)

    def start(self):
        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=self.capability,
                                  live=True)
        self.ws.start_nonblocking()

    def stop(self):
        try:
            self.ws.join()
        except AttributeError:
            # If self.ws has not been instantiated
            pass

    def set_login_settings(self, host, port, chan, nick, auth):
        self.host = host
        self.port = port
        self.chan = chan
        self.nick = nick
        self.auth = auth

    def set_settings(self, host, port, chan, nick, auth, denied_users, allowed_ranks, allowed_people):
        self.set_login_settings(host, port, chan, nick, auth)
        self.denied_users = denied_users
        self.allowed_ranks = allowed_ranks
        self.allowed_people = allowed_people
    
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

    def message_handler(self, m):
        try:
            if m.type == "376":
                self.app.add_message("Successfully logged in as: {}.".format(self.nick), True)
            elif m.type == "CAP * ACK":
                self.app.add_message("Successfully added requirement: {}.".format(", ".join(m.message.split("/")[1:])), True)
            elif m.type == "366":
                self.app.add_message("Successfully joined: {}\nBot is active now.".format(self.chan), True)
                logging.info(f"Successfully joined channel: #{m.channel}")
            
            elif m.type == 'USERNOTICE':
                # If someone Subscribes, Gift Bombs or Gift Subs, and the corresponding setting is set to true.
                if (m.tags["msg-id"] in ["subgift", "anonsubgift"] and self.sub_gift) or \
                (m.tags["msg-id"] in ["sub", "resub", "giftpaidupgrade", "anongiftpaidupgrade"] and self.sub) or \
                (m.tags["msg-id"] in ["submysterygift", "anonsubmysterygift"] and self.sub_gift_bomb):
                    self.app.add_message(m.tags["system-msg"].replace("\\s", " "), True)

            elif m.type == "NOTICE":
                logging.info(m.message)
                self.app.add_message("Notice: " + m.message, True)
                
            elif m.type == "PRIVMSG":
                # Look for commands.
                if m.message.startswith("!average") and self.check_permissions(m):
                    self.command_average(m)
                elif m.message.startswith("!vote") and self.check_permissions(m):
                    self.command_vote(m)
                else:
                    # Parse message for potential numbers/votes.
                    self.check_for_numbers(m.message, m.user)
                    self.check_for_text(m.message, m.user)
        except Exception as e:
            logging.error(e)

    def check_permissions(self, m):
        for rank in self.allowed_ranks:
            if rank in m.tags["badges"]:
                return True
        for name in self.allowed_people:
            if m.user.lower() == name.lower():
                return True
        return False

    def check_denied_users(self, sender):
        # Check if sender is not a denied user (generally another bot).
        return sender in self.denied_users

    def command_average(self, m):
        # Calculate Average and send output message.
        if self.parse_command(m.message, "Average"):
            self.messages["Nr"] = {i: self.messages["Nr"][i] for i in self.messages["Nr"] if i == '0' or (self.messages["Nr"][i].timestamp + 60 > time.time() and self.messages["Nr"][i].message >= self.min and self.messages["Nr"][i].message <= self.max)}
            if len(self.messages["Nr"]) > 0:
                # Calculate Average.
                average = 0
                for i in self.messages["Nr"]:
                    average += int(self.messages["Nr"][i].message)
                average /= len(self.messages["Nr"])
                
                # Send outputs.
                out = "/me Average is {:.2f}{}.".format(average, "%" * (self.max == 100))
                if self.average_results:
                    self.app.add_message(out, True)
                self.messages["Nr"] = {}
            else:
                out = "No recent numbers found to take the average from."
                if self.average_command_errors:
                    self.app.add_message(out, True)
            logging.info(out)
            self.ws.send_message(out)

    def command_vote(self, m):
        # Calculate what vote won and send output message.
        self.messages["Txt"] = {i: self.messages["Txt"][i] for i in self.messages["Txt"] if self.messages["Txt"][i].timestamp + 60 > time.time()}
        
        # Find out whether sender wants to vote using numbers or letters.
        t = "Txt"
        if len(m.message) > 6:
            if self.parse_command(m.message, "Vote"):
                self.messages["Nr"] = {i: self.messages["Nr"][i] for i in self.messages["Nr"] if self.messages["Nr"][i].timestamp + 60 > time.time() and self.messages["Nr"][i].message >= self.min and self.messages["Nr"][i].message <= self.max}
                t = "Nr"
            else:
                return
        self.vote(t)
    
    def vote(self, t):
        if len(self.messages[t]) > 0:
            # Turn votes into a standard dictionary.
            votes = {}
            total = 0
            for i in self.messages[t]:
                if self.messages[t][i].message in votes:
                    votes[self.messages[t][i].message] += 1
                else:
                    votes[self.messages[t][i].message] = 1
                total += 1
            # Get votes amount in list format.
            listvotes = [votes[i] for i in list(votes)]
            # Get indexes of winning votes.
            indexes = [i for i, j in enumerate(listvotes) if j == max(listvotes)]
            # Send outputs.
            if len(indexes) == 1:
                out = "/me {} won with {:.2f}%.".format(list(votes)[indexes[0]], listvotes[indexes[0]] / total * 100)#, "(" + ", ".join(["{}:{}".format(i, votes[i]) for i in list(votes)]) + ")"))
            else:
                out = "/me " + ", ".join([i[1] for i in enumerate(list(votes)) if i[0] in indexes[:-1]]) + " and " + list(votes)[indexes[-1]] + " tied with {:.2f}%.".format(listvotes[indexes[0]] / total * 100)# + " {}".format("(" + ", ".join(["{}:{}".format(i, votes[i]) for i in list(votes)]) + ")"))
            if self.voting_results:
                self.app.add_message(out, True)
            logging.info(out)
            self.ws.send_message(out)
            self.messages[t] = {}
        else:
            out = "No votes found."
            logging.info(out)
            # This will fail if the user pressed Vote on the GUI without the bot running.
            # However, it does not crash the program, and does not obstruct the program
            self.ws.send_message(out)
            if self.voting_command_errors:
                self.app.add_message(out, True)

    def parse_number(self, message, sender):
        # Stripping message potentially containing a number of illegal characters.
        if self.check_denied_users(sender):
            return "False"
        remove = {"%":"", ",":"."}
        for i in remove:
            message = message.replace(i, remove[i])
        message = message.split("/")
        for m in message:
            try:
                m = float(m)
                return m
            except ValueError:
                pass
        return "False"

    def parse_command(self, message, t):
        # Extract parameters from a command.
        try:
            self.min = float(str.split(message)[1])
            self.max = float(str.split(message)[2])
            if self.min >= self.max:
                out = "Max parameter should be larger than Min parameter"
                logging.info(out)
                if t == "Vote" and self.voting_command_errors or t == "Average" and self.average_command_errors:
                    self.app.add_message(out, True)
                self.ws.send_message(out)
                self.min = -1
                self.max = -1
            else:
                return True
        except:
            out = "Parameter Error"
            if t == "Vote" and self.voting_command_errors or t == "Average" and self.average_command_errors:
                self.app.add_message(out, True)
            logging.info(out)
            self.ws.send_message(out)
        return False

    def check_for_numbers(self, message, sender):
        # Check if the message contains a number.
        for m in message.split():
            msg = self.parse_number(m, sender)
            if msg != "False":
                if self.numbers:
                    self.app.add_message(msg)
                self.messages["Nr"][sender] = Messages(sender, msg)
                break

    def check_for_text(self, message, sender):
        # Check if the message contains a vote.
        if self.check_denied_users(sender):
            return
        msg = message.split()
        if msg[0][0].upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and msg[0].upper() == len(msg[0]) * msg[0][0].upper():
            # Remove "I will/can/do" messages.
            if msg[0][0].upper() == "I" and len(msg) > 1 and len(msg[1]) > 2:
                return
            # Remove "D I A L".
            if len([i for i in msg if len(i) == 1]) == len(msg) and "".join(msg) != len("".join(msg)) * msg[0]:
                return
            if self.votes:
                self.app.add_message(msg[0][0].upper())
            self.messages["Txt"][sender] = Messages(sender, msg[0][0].upper())

if __name__ == "__main__":
    bot = CubieBot()

    app = App(bot)

    bot.app = app
