# TwitchCubieBotGUI
Twitch Bot focusing on aggregating votes and averages from Twitch chat, with a GUI

---
# Explanation
When the bot has started, it will start listening to chat messages in the channel listed in the settings.txt file. All messages will be parsed, and votes and numbers will be stored for 3 minutes after the messages comes in.
If at some point someone decides to calculate a vote or average, the information from the last 3 minutes will be used. <b>This means it is not needed to start a vote or average in advance</b> Note that if one user sends multiple votes or multiple values, newer values will override the older ones, so everyone only has one vote.

This is an extention of my existing [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot) program, but now with a convenient and simple GUI:
![image](https://user-images.githubusercontent.com/37621491/59962273-5ec58200-94e3-11e9-9d85-3cb54c15f6f1.png)

An explanation of this GUI will be provided below the explanation of the bot itself. 

---
# Voting
Commands:
<pre>
<b>!vote</b>
</pre>
This command will decide the winner between votes.
<pre>
<b>!vote numbers</b>
</pre>
This command will decide the winner between numbers.
<pre>
<b>!vote emotes</b>
</pre>
This command will decide the winner between emotes.

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
The logging and chat output when `!vote numbers` was typed by someone with the appropriate rank:
<pre>
<b>3.0 won with 84.72%.</b>
</pre>

The logging and chat output when `!average 0 100` was typed by someone with the appropriate rank:
<pre>
<b>Average is 67.38%.</b>
</pre>

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
    "LookbackTime": 30,
    "AllowedPeople": [],
    "Sub": 1,
    "SubGiftBomb": 1,
    "SubGift": 1,
    "AverageResults": 1,
    "AverageCommandErrors": 1,
    "VotingResults": 1,
    "Votes": 1,
    "VotingCommandErrors": 1,
    "Numbers": 1,
    "SaveChat": 0
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
| LookbackTime | The amount of seconds the bot looks back for votes/numbers/emotes. | 30 |

Everything below this point is linked to the Settings page of the GUI, explained below.

*Note that the example OAuth token is not an actual token, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---
# GUI
Some of the values from the settings.txt file can also be edited in the GUI. 
For reference, this is the GUI:

![image](https://user-images.githubusercontent.com/37621491/59962273-5ec58200-94e3-11e9-9d85-3cb54c15f6f1.png)

Let's clarify the functionality from the GUI:

| **Button** | **Action** |
| ---------- | ----------- |
| Auth | This button will hide or unhide your Authentication token. This way you can hide it when you aren't changing it, so that it will not leak. |
| Stop | This button is both "Stop" and "Run" at the same time. When the bot is running, the button will say Stop. While it is not, it will display "Run". Pressing this button will either stop the bot from running, or start the bot using the information filled in above. | 
| Clear | Clears the console below |
| Vote | Equivalent to typing `!vote` in chat. Calls a vote. |
| Settings | Opens up a popup message, as shown on the left side in the screenshot. |
| Save & Close | Closes the setting popup message, and saves the settings. |

Note that the settings in the popup message refer to what will be shown in the console in the main GUI. This is the meaning of each section:

| **Name** | **Meaning** |
| -------- | ----------- |
| Sub | If regular subscriptions should show up in the message box. |
| Sub Gift Bomb | If sub mystery gifts (a handful subscriptions gifted to several randomly picked users) should show up in the message box. |
| Sub Gift | If regular subscription gifts should show up in the message box. |
| Average Results | If the results from `!average min max` should show up in the message box. |
| Average Cmd Errors | If errors from incorrect usages of `!average` should show up in the message box. Eg: `No recent numbers found to take the average from` or `Max parameter should be larger than Min parameter`. |
| Vote Results | If the results from `!vote min max` or `!vote` should show up in the message box. |
| Votes | If individual votes should show up in the message box. Eg: `A` or `Y`. |
| Vote Cmd Errors | If errors from incorrect usages of `!vote min max` or `!vote` should show up in the message box. Eg: `No votes found.` or `Max parameter should be larger than Min parameter`. |
| Numbers | If individual numbers should show up in the message box. Eg: `23.0` or `12.4`. |

---

# Requirements
* Python 3+ (Only tested on 3.6)

Download Python online.

* TwitchWebsocket

Install this using `pip install git+https://github.com/CubieDev/TwitchWebsocket.git`

* TwitchCubieBot

Install this using `pip install git+https://github.com/CubieDev/TwitchCubieBot.git`

This last library is my own [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) wrapper, which makes making a Twitch chat bot a lot easier.
This repository can be seen as an implementation using this wrapper.

---

# Other Twitch Bots

* [TwitchGoogleTranslate](https://github.com/CubieDev/TwitchGoogleTranslate)
* [TwitchMarkovChain](https://github.com/CubieDev/TwitchMarkovChain)
* [TwitchRhymeBot](https://github.com/CubieDev/TwitchRhymeBot)
* [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot)
* [TwitchDeathCounter](https://github.com/CubieDev/TwitchDeathCounter)
* [TwitchSuggestDinner](https://github.com/CubieDev/TwitchSuggestDinner)
* [TwitchPickUser](https://github.com/CubieDev/TwitchPickUser)
* [TwitchSaveMessages](https://github.com/CubieDev/TwitchSaveMessages)
* [TwitchMMLevelPickerGUI](https://github.com/CubieDev/TwitchMMLevelPickerGUI) (Mario Maker 2 specific bot)
* [TwitchMMLevelQueueGUI](https://github.com/CubieDev/TwitchMMLevelQueueGUI) (Mario Maker 2 specific bot)
* [TwitchPackCounter](https://github.com/CubieDev/TwitchPackCounter) (Streamer specific bot)
* [TwitchDialCheck](https://github.com/CubieDev/TwitchDialCheck) (Streamer specific bot)
* [TwitchSendMessage](https://github.com/CubieDev/TwitchSendMessage) (Not designed for non-programmers)
