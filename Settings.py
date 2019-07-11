
import logging, json, os, sys
logger = logging.getLogger(__name__)

class Settings:
    """ Loads data from settings.txt into the bot """
    
    PATH = os.path.join(sys.path[0], "settings.txt")
    
    def get_settings(self):
        logger.debug("Loading settings.txt file...")
        try:
            # Try to load the file using json.
            # And pass the data to the Bot class instance if this succeeds.
            with open(Settings.PATH, "r") as f:
                settings = f.read()
                settings_dict = json.loads(settings)
                logger.debug("Settings loaded into Bot.")
                return [settings_dict[key] for key in settings_dict]

        except ValueError:
            logger.error("Error in settings file.")
            raise ValueError("Error in settings file.")

        except FileNotFoundError:
            # If the file is missing, create a standardised settings.txt file
            # With all parameters required.
            logger.error("Please fix your settings.txt file that was just generated.")
            with open(Settings.PATH, 'w') as f:
                standard_dict = {
                                    "Host": "irc.chat.twitch.tv",
                                    "Port": 6667,
                                    "Channel": "#<channel>",
                                    "Nickname": "<name>",
                                    "Authentication": "oauth:<auth>",
                                    "DeniedUsers": ["streamelements", "marbiebot", "moobot"],
                                    "AllowedRanks": ["broadcaster", "moderator"],
                                    "AllowedPeople": [],
                                    "LookbackTime": 30,
                                    "Sub": 0,
                                    "SubGiftBomb": 1,
                                    "SubGift": 1,
                                    "AverageResults": 1,
                                    "AverageCommandErrors": 0,
                                    "VotingResults": 1,
                                    "Votes": 1,
                                    "VotingCommandErrors": 1,
                                    "Numbers": 1
                                }
                f.write(json.dumps(standard_dict, indent=4, separators=(',', ': ')))
                raise ValueError("Please fix your settings.txt file that was just generated.")
    
    @staticmethod
    def update(bot):
        with open(Settings.PATH, 'w') as f:
            standard_dict = {
                                "Host": bot.host,
                                "Port": bot.port,
                                "Channel": bot.chan,
                                "Nickname": bot.nick,
                                "Authentication": bot.auth,
                                "DeniedUsers": bot.denied_users,
                                "AllowedRanks": bot.allowed_ranks,
                                "AllowedPeople": bot.allowed_people,
                                "LookbackTime": bot.lookback_time,
                                "Sub": bot.sub,
                                "SubGiftBomb": bot.sub_gift_bomb,
                                "SubGift": bot.sub_gift,
                                "AverageResults": bot.average_results,
                                "AverageCommandErrors": bot.average_command_errors,
                                "VotingResults": bot.voting_results,
                                "Votes": bot.votes,
                                "VotingCommandErrors": bot.voting_command_errors,
                                "Numbers": bot.numbers
                            }
            f.write(json.dumps(standard_dict, indent=4, separators=(',', ': ')))
