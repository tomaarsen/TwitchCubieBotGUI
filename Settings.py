
import logging, json
logger = logging.getLogger(__name__)

class Settings:
    """ Loads data from settings.txt into the bot """
    def __init__(self, bot):
        logger.debug("Loading settings.txt file...")
        try:
            # Try to load the file using json.
            # And pass the data to the Bot class instance if this succeeds.
            with open("settings.txt", "r") as f:
                settings = f.read()
                data = json.loads(settings)
                data = json.loads(settings)
                bot.set_settings(data['Host'],
                                data['Port'],
                                data['Channel'],
                                data['Nickname'],
                                data['Authentication'],
                                data["DeniedUsers"],
                                data["AllowedRanks"],
                                data["AllowedPeople"]
                                )
                bot.set_user_settings(
                                data["Sub"],
                                data["SubGiftBomb"],
                                data["SubGift"],
                                data["AverageResults"],
                                data["AverageCommandErrors"],
                                data["VotingResults"],
                                data["Votes"],
                                data["VotingCommandErrors"],
                                data["Numbers"]
                                )
                logger.debug("Settings loaded into Bot.")
        except ValueError:
            logger.error("Error in settings file.")
            raise ValueError("Error in settings file.")
        except FileNotFoundError:
            # If the file is missing, create a standardised settings.txt file
            # With all parameters required.
            logger.error("Please fix your settings.txt file that was just generated.")
            with open('settings.txt', 'w') as f:
                standard_dict = {
                                    "Host": "irc.chat.twitch.tv",
                                    "Port": 6667,
                                    "Channel": "#<channel>",
                                    "Nickname": "<name>",
                                    "Authentication": "oauth:<auth>",
                                    "DeniedUsers": ["streamelements", "marbiebot", "moobot"],
                                    "AllowedRanks": ["broadcaster", "moderator"],
                                    "AllowedPeople": [],
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
        with open('settings.txt', 'w') as f:
            standard_dict = {
                                "Host": bot.host,
                                "Port": bot.port,
                                "Channel": bot.chan,
                                "Nickname": bot.nick,
                                "Authentication": bot.auth,
                                "DeniedUsers": bot.denied_users,
                                "AllowedRanks": bot.allowed_ranks,
                                "AllowedPeople": bot.allowed_people,
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
