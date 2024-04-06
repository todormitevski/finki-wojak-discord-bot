# Discord Bot: FINKI Wojak

## Overview
FINKI Wojak is a Python-based Discord bot designed to manage interactions within a small private Discord server. It offers various features to enhance server engagement and utility, including greetings, farewells, random number generation, motivational quote fetching, sentiment analysis of user messages, voice channel management, and more.

## Features
- **Slash Commands**: Users can utilize slash commands to access a list of available commands.
- **Regular Commands**: Includes commands for greetings, farewells, generating random numbers, displaying motivational quotes, and counting profanities.
- **Voice Channel Management**: Commands to join, leave, play, and stop audio in voice channels.
- **Sentiment Analysis**: Assess the mood of specified users based on their recent messages.
- **Word Filtering**: Automatically detects and deletes messages containing banned words.
- **Developer Command**: A command specifically for developers to purge spam messages.
- **Message Logging**: Logs user messages to keep track of user interactions and server activity.

## Setup
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Obtain necessary API tokens and Discord user ID.
4. Replace empty strings in `apikeys.py` with appropriate tokens.
5. Replace `AUTHORID` in `apikeys.py` with your Discord user ID.
6. Run `main.py` to start the bot.

## Commands
- **/help**: View all usable commands.
- **$zdravo**: Greet others.
- **$cao**: Bid farewell.
- **$frlikocka**: Generate a random number between 1 and 6.
- **$mudrost**: Display a motivational quote.
- **$wordcount**: Display the number of profanities cleared.
- **$mood @user**: Assess the mood of the mentioned user based on recent messages.
- **$maus**, **$vino**: Superstition commands for luck before exams.
- **$join**: Join a voice channel.
- **$dc**: Leave a voice channel.
- **$play [media_name]**: Play audio in the voice channel.
- **$stop**: Stop playing media.
- **$purge [amount]**: Delete spam messages (developer command).

## Contributing
Contributions are welcome! Feel free to fork the repository, make changes, and submit pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
