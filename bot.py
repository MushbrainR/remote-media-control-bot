import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Functions to control media playback on macOS using AppleScript
def play_pause():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke space'])

def forward_10_seconds():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 124'])  # right arrow key

def back_10_seconds():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 123'])  # left arrow key

def volume_up():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 126'])  # up arrow key

def volume_down():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 125'])  # down arrow key

# Async Telegram bot commands
async def start(update: Update, context):
    # Create a persistent inline keyboard for media controls
    keyboard = [
        [InlineKeyboardButton("⏯ Play/Pause", callback_data='play')],
        [InlineKeyboardButton("⏩ Forward 10s", callback_data='forward')],
        [InlineKeyboardButton("⏪ Back 10s", callback_data='back')],
        [InlineKeyboardButton("🔊 Volume Up", callback_data='volume_up')],
        [InlineKeyboardButton("🔉 Volume Down", callback_data='volume_down')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with the keyboard that remains on screen
    if update.message:
        await update.message.reply_text("Control your media:", reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text("Control your media:", reply_markup=reply_markup)

# Callback handler for button presses
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    # Determine which button was pressed and call the appropriate function
    if query.data == 'play':
        play_pause()
        await query.edit_message_text("Play/Pause toggled.", reply_markup=await build_keyboard())
    elif query.data == 'forward':
        forward_10_seconds()
        await query.edit_message_text("Skipped forward 10 seconds.", reply_markup=await build_keyboard())
    elif query.data == 'back':
        back_10_seconds()
        await query.edit_message_text("Rewound 10 seconds.", reply_markup=await build_keyboard())
    elif query.data == 'volume_up':
        volume_up()
        await query.edit_message_text("Volume increased.", reply_markup=await build_keyboard())
    elif query.data == 'volume_down':
        volume_down()
        await query.edit_message_text("Volume decreased.", reply_markup=await build_keyboard())

# Function to generate the inline keyboard (keeps the buttons on the screen)
async def build_keyboard():
    keyboard = [
        [InlineKeyboardButton("⏯ Play/Pause", callback_data='play')],
        [InlineKeyboardButton("⏩ Forward 10s", callback_data='forward')],
        [InlineKeyboardButton("⏪ Back 10s", callback_data='back')],
        [InlineKeyboardButton("🔊 Volume Up", callback_data='volume_up')],
        [InlineKeyboardButton("🔉 Volume Down", callback_data='volume_down')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Main function to initialize the bot
def main():
    # Telegram bot API token (replace with your bot token)
    TOKEN = 'YOUR_TOKEN_HERE'

    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot with polling (no await needed)
    application.run_polling()

if __name__ == '__main__':
    main()