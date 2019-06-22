# TwitchCubieBotGUI
Twitch Bot focusing on aggregating votes and averages from Twitch chat, with a GUI

---
# Explanation
When the bot has started, it will start listening to chat messages in the channel listed in the settings.txt file. All messages will be parsed, and votes and numbers will be stored for 3 minutes after the messages comes in.
If at some point someone decides to calculate a vote or average, the information from the last 3 minutes will be used. <b>This means it is not needed to start a vote or average in advance</b> Note that if one user sends multiple votes or multiple values, newer values will override the older ones, so everyone only has one vote.

This is an extention of my existing [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot) program, but now with a convenient and simple GUI:


---
# Voting
Commands:
<pre>
<b>!vote</b>
</pre>
This command will decide the winner between votes.
<pre>
<b>!vote min max</b>
</pre>
This command will decide the winner between numbers higher than min, and lower than max.

Valid votes (for A) include:
* A
* AAAAA
* A A A
* A Please
* All of the above, but with lower case a

Invalid votes include:
* I would really like that
* D I A L

Any single letter can be a vote.

# Averaging
Command:
<pre>
<b>!average min max</b>
</pre>
This command will average all numbers between min and max send in the last 3 minutes.

---
# Examples

The logging and chat output when `!vote` was typed by someone with the appropriate rank:
<pre>
<b>B won with 74.24%.</b>
</pre>
The logging and chat output when `!vote 0 10` was typed by someone with the appropriate rank:
<pre>
<b>3.0 won with 84.72%.</b>
</pre>

The logging and chat output when `!average 0 100` was typed by someone with the appropriate rank:
<pre>
<b>Average is 67.38%.</b>
</pre>

---

# Requirements
* TwitchWebsocket

Install this using `pip install git+https://github.com/CubieDev/TwitchWebsocket.git`

This last library is my own [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) wrapper, which makes making a Twitch chat bot a lot easier.
This repository can be seen as an implementation using this wrapper.

---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>",
    "DeniedUsers": [
        "streamelements",
        "marbiebot",
        "moobot"
    ],
    "AllowedRanks": [
        "broadcaster",
        "moderator"
    ],
    "AllowedPeople": []
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#CubieDev" |
| Nickname             | The Username of the bot account.                                  | "CubieB0T" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |
| DeniedUsers     | List of (bot) names who's messages will not be included in voting and averages. | ["streamelements", "marbiebot", "moobot"] |
| AllowedRanks  | List of ranks required to be able to perform the commands. | ["broadcaster", "moderator"] |
| AllowedPeople | List of users who, even if they don't have the right ranks, will be allowed to perform the commands. | ["cubiedev"] |

*Note that the example OAuth token is not an actual token, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---

# Other Twitch Bots

* [TwitchGoogleTranslate](https://github.com/CubieDev/TwitchGoogleTranslate)
* [TwitchMarkovChain](https://github.com/CubieDev/TwitchMarkovChain)
* [TwitchRhymeBot](https://github.com/CubieDev/TwitchRhymeBot)
* [TwitchDeathCounter](https://github.com/CubieDev/TwitchDeathCounter)
* [TwitchSuggestDinner](https://github.com/CubieDev/TwitchSuggestDinner)
* [TwitchPickUser](https://github.com/CubieDev/TwitchPickUser)
* [TwitchSaveMessages](https://github.com/CubieDev/TwitchSaveMessages)
* [TwitchPackCounter](https://github.com/CubieDev/TwitchPackCounter) (Streamer specific bot)
* [TwitchDialCheck](https://github.com/CubieDev/TwitchDialCheck) (Streamer specific bot)
* [TwitchSendMessage](https://github.com/CubieDev/TwitchSendMessage) (Not designed for non-programmers)
