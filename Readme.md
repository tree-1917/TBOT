# 📚 Telegram Bot for Teacher and Student Interaction

This Telegram bot allows teachers to upload topics (PDFs and audio files) with unique identifiers, and students to access and download these topics. The bot features separate functionalities for teachers and students and includes commands for resetting the chat and restarting the interaction.

## ✨ Features

- **🚀 Start and Restart Interaction**: Users can initiate and reset their interaction with the bot using `/start` and `/restart` commands.
- **👳‍♂️ Teacher Mode**: Allows teachers to upload topics (PDFs and audio files) with specific identifiers.
- **👨‍🎓 Student Mode**: Allows students to view and download available topics by referencing the identifiers.
- **🔘 Commands and Button Interactions**: User-friendly interface with buttons for easier interaction.

## 📋 Prerequisites

- Python 3.6+
- Telegram bot token (create a bot using [BotFather](https://core.telegram.org/bots#botfather))

## 🛠️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/telegram-bot-teacher-student.git
   cd telegram-bot-teacher-student
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory and add your bot token:

   ```env
   TOKEN_API=your-telegram-bot-token
   ```

## 🏃 Usage

1. Run the bot:

   ```bash
   python bot.py
   ```

2. Open Telegram and start a chat with your bot.

3. Use the `/start` command to begin the interaction.

4. Choose whether you are a teacher or a student by clicking the appropriate button.

### 👩‍🏫 Teacher Mode

1. Click the "upload topic" button.
2. Upload a PDF or audio file with the caption format: `#light #Source_id #Source_name`.

### 👨‍🎓 Student Mode

1. Click the "topics" button to view available topics.
2. Click the identifier of the topic you want to download.

## 🔄 Resetting the Interaction

If you need to reset the interaction, use the `/restart` command. This will clear any ongoing interaction and allow you to start fresh.

## 🗂️ Project Structure

```shell
    telegram-bot-teacher-student/
            │
            ├── bot.py # Main bot script
            ├── .env # Environment file containing the bot token
            ├── requirements.txt # Required Python packages
            └── README.md # Project documentation
```

## 🌟 Contributing

Feel free to contribute to this project by opening issues or submitting pull requests. Contributions are welcome!

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
