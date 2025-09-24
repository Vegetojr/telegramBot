from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import sqlite3
import random
import time
# CLASS THAT HANDLES THE DATABASE AND ITS INFO


class Character:
    def __init__(self, id_number=-1, name="", path=""):
        self.id_number = id_number
        self.name = name
        self.path = path
        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()

    def select_hiragana(self, id_number):

        self.cursor.execute(
            """SELECT * FROM hiragana WHERE id = {}""".format(id_number))
        results = self.cursor.fetchone()

        self.id_number = id_number
        self.name = results[1]
        self.path = results[2]

    def select_katakana(self, id_number):
        self.cursor.execute(
            """SELECT * FROM katakana WHERE id = {}""".format(id_number))
        results = self.cursor.fetchone()

        self.id_number = id_number
        self.name = results[1]
        self.path = results[2]


class Response:
    def __init__(self, id_number=-1, question="", error="", noAnswer="", quizStarted="", quizStoped="", quizAlreadyStrated="", quziAlreadyStoped="", correct="", incorrect='', stat='', idstat='', cooldown=''):
        self.id_number = id_number
        self.question = question
        self.error = error
        self.noAnswer = noAnswer
        self.quizStarted = quizStarted
        self.quizStoped = quizStoped
        self.quizAlreadyStrated = quizAlreadyStrated
        self.quziAlreadyStoped = quziAlreadyStoped
        self.correct = correct
        self.incorrect = incorrect
        self.stat = stat
        self.idstat = idstat
        self.cooldown = cooldown
        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()

    def loadResponse(self, id_number):
        self.cursor.execute(
            """SELECT * FROM tsundereResponses WHERE id = {} """.format(id_number))
        results = self.cursor.fetchone()
        self.question = results[1]
        self.error = results[2]
        self.noAnswer = results[3]
        self.quizStarted = results[4]
        self.quizStoped = results[5]
        self.quizAlreadyStrated = results[6]
        self.quziAlreadyStoped = results[7]
        self.correct = results[8]
        self.incorrect = results[9]
        self.stat = results[10]
        self.idstat = results[11]
        self.cooldown = results[12]


class Stat:
    def __init__(self, id_chat=-1, id_char=-1, correcto=-1, incorrecto=-1):
        self.id_chat = id_chat
        self.id_char = id_char
        self.correcto = correcto
        self.incorrecto = incorrecto
        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()

    def statHiragana(self, id_chat, id_char):
        self.cursor.execute(
            ''' SELECT correcto, incorrecto FROM player_hiragana_stats WHERE player_id = {} AND hiragana_id = {}'''.format(id_chat, id_char))
        results = self.cursor.fetchone()
        if results:
            self.correcto = results[0]
            self.incorrecto = results[1]
            self.id_char = id_char

    def statKatakana(self, id_chat, id_char):
        self.cursor.execute(
            ''' SELECT correcto, incorrecto FROM player_katakana_stats WHERE player_id = {} AND katakana_id = {}'''.format(id_chat, id_char))
        results = self.cursor.fetchone()
        if results:
            self.correcto = results[0]
            self.incorrecto = results[1]
            self.id_char = id_char


def random_number_conversation():
    return random.randint(1, 20)


def random_number_46():
    return random.randint(1, 46)


conversation = Response()
stadistics = Stat()
TOKEN = '7221596048:AAFRaeuqHK48_8lZUNJ76Adz6EjJI35peBY'
BOT_NAME = '@JapChar_bot'
ASKING_CHAR = range(1)

# commands


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '''STARTED THE CONVESATION
            \nTo begin interacting with the bot you need to use  /  to start the commands
            \n/help - shows list of commands
           ''')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
                                    \n/starthiragana - starts the hiragana quiz. You'll have 30 seconds to answer. Every question will show up 1 minute after you answered or not
                                    \n/startkatakana - same but with the katakana quiz
                                    \n/stopquiz - stops the quiz you're currently in. Once you stop the quiz you'll have to WAIT 90 SECONDS before starting other quiz
                                    \n/proggreshiraganaglobal - shows all progress of hiragana
                                    \n/proggreskatakanaglobal - shows all progress of katakana
                                    \n/proggreshiraganaid - shows progress of 1 hiragana character
                                    \n/proggreskatakanaid - shows progress of 1 katakana character
                                    \n\n IF YOU ENCOUNTER A BUG WITH THE QUIZES JUST STOP THE QUIZ AND WAIT UNTIL YOU CAN START OTHER ONE
                                    ''')


async def proggresKatakana_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT sum(correcto),sum(incorrecto) FROM player_katakana_stats WHERE player_id ={} '.format(chat_id))
    results = cursor.fetchone()
    conn.close()

    if results == (None, None):
        await update.message.reply_text('You haven`t started learning katakanas')

    else:
        conversation.loadResponse(random_number_conversation())
        correcto = results[0]
        incorrecto = results[1]
        total = correcto + incorrecto
        rate = (correcto / total * 100) if total else 0.0
        await update.message.reply_text(
            f'Category: Katakana \n'
            f'Correct: {correcto}\n'
            f'Incorrect: {incorrecto}\n'
            f'WinRate: {rate:.2f}%',
        )
        await context.bot.send_message(chat_id=chat_id, text=conversation.stat, parse_mode="MarkdownV2")


async def proggresHiragana_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT sum(correcto),sum(incorrecto) FROM player_hiragana_stats WHERE player_id ={} '.format(chat_id))
    results = cursor.fetchone()
    conn.close()

    if results == (None, None):
        await update.message.reply_text('You haven`t started learning hiraganas')

    else:
        conversation.loadResponse(random_number_conversation())
        correcto = results[0]
        incorrecto = results[1]
        total = correcto + incorrecto
        rate = (correcto / total * 100) if total else 0.0
        await update.message.reply_text(
            f'Category: Hiragana \n'
            f'Correct: {correcto}\n'
            f'Incorrect: {incorrecto}\n'
            f'WinRate: {rate:.2f}%',
        )
        await context.bot.send_message(chat_id=chat_id, text=conversation.stat, parse_mode="MarkdownV2")


async def proggresKatakanaID_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["progress_type"] = "katakana"
    await update.message.reply_text('Which katakana character would you like to know your stats for?')
    return ASKING_CHAR

# ESTO ESTA MAL EN ALGUN LADO NO TENGO NI IDEA QUE


async def proggresHiraganaID_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["progress_type"] = "hiragana"
    await update.message.reply_text('Which hiragana would you like to know your stats for?')
    return ASKING_CHAR  # ← Este es el estado al que pasamos


async def handle_progress_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    letter = update.message.text.strip().lower()
    progress_type = context.user_data.get("progress_type",)
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    if progress_type == "hiragana":
        cursor.execute(
            'SELECT id,path FROM hiragana WHERE nombre = ?', (letter,))
    else:
        cursor.execute(
            'SELECT id,path FROM katakana WHERE nombre = ?', (letter,))

    result = cursor.fetchone()
    conn.close()

    if result is None:
        await update.message.reply_text(f'No character "{letter}" found in the {progress_type} database.')
        return ConversationHandler.END

    conversation.loadResponse(random_number_conversation())
    id_char = result[0]
    image_path = result[1]
    if progress_type == "hiragana":
        stadistics.statHiragana(chat_id, id_char)
    else:
        stadistics.statKatakana(chat_id, id_char)

    total = stadistics.correcto + stadistics.incorrecto
    rate = (stadistics.correcto / total * 100) if total else 0.0

    with open(image_path, 'rb') as image_file:
        await context.bot.send_photo(chat_id=chat_id, photo=image_file, parse_mode="MarkdownV2")

    await update.message.reply_text(
        f'Character: {letter}\n'
        f'Correct: {stadistics.correcto}\n'
        f'Incorrect: {stadistics.incorrecto}\n'
        f'WinRate: {rate:.2f}%'
    )
    await context.bot.send_message(chat_id=chat_id, text=conversation.idstat, parse_mode="MarkdownV2")
    return ConversationHandler.END


async def send_image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    ch = Character()  # Instantiate here to grab the latest image path
    ch.select_hiragana(1)  # or whatever ID you want to send
    image_path = ch.path

    with open(image_path, 'rb') as image_file:
        await update.message.reply_text('wanna now what`s EPIC')
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_file,
            caption="THATS EPIC"  # Optional caption
        )


def handle_response(text: str) -> str:
    processed: str = text.lower()
    if "hello" in text:
        return "Hallo, I'm emu otori"
    if 'how are you' in text:
        return 'emu is meaning smile'
    if 'the wonder stage' in text:
        return 'yokoso kira kira'
    return 'the wonder stage'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    text: str = update.message.text

    message_type: str = update.message.chat.type

    if message_type == "group":
        if BOT_NAME in text:
            new_text: str = text.replace(BOT_NAME, "").strip()
            response: str = handle_response(new_text)
    else:
        response: str = handle_response(text)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update {update} caused error {context.error}")

# LOGIC OF THE QUESTIONS


async def ask_question(context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["can_answer"] = True
    quiz_type = context.chat_data.get("quiz_type", "hiragana")
    is_running = context.chat_data.get("quiz_running", False)
    timer = 30.0
    if not is_running:
        return

    question_id = random_number_46()
    context.chat_data["current_question_id"] = question_id

    ch = Character()
    if quiz_type == "hiragana":
        ch.select_hiragana(question_id)
    else:
        ch.select_katakana(question_id)

    conversation.loadResponse(random_number_conversation())

    chat_id = context.job.chat_id
    image_path = ch.path
    question_text = conversation.question

    context.chat_data["expected_answer"] = ch.name
    context.chat_data["answered"] = False

    try:
        with open(image_path, 'rb') as image_file:
            await context.bot.send_photo(chat_id=chat_id, photo=image_file, caption=question_text, parse_mode="MarkdownV2")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=conversation.error, parse_mode="MarkdownV2")
        return

    if is_running:
        job = context.job_queue.run_once(
            check_response, when=timer, chat_id=chat_id)
        context.chat_data["current_job"] = job


async def check_response(context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["can_answer"] = False
    chat_id = context.job.chat_id
    answered = context.chat_data.get("answered", False)
    current_question_id = context.chat_data.get("current_question_id", -1)
    timer = 60
    is_running = context.chat_data.get("quiz_running", False)
    if not is_running:
        return

    if not answered:
        if not is_running:
            return
        if current_question_id == -1:
            return
        conversation.loadResponse(random_number_conversation())
        await context.bot.send_message(chat_id=chat_id, text=conversation.noAnswer, parse_mode="MarkdownV2")

    if is_running:
        context.job_queue.run_once(ask_question, when=timer, chat_id=chat_id)


async def start_hiragana_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cooldown = 60*1.52
    last_stopped = context.chat_data.get("last_quiz_stop_time", 0)
    elapsed = time.time() - last_stopped
    conversation.loadResponse(random_number_conversation())
    if elapsed < cooldown:
        await update.message.reply_text(
            f"{conversation.cooldown} \nWait  {int(cooldown - elapsed)} seconds",
            parse_mode="MarkdownV2"
        )
        return

    if context.chat_data.get("quiz_running", False):
        running_type = context.chat_data.get("quiz_type", "")
        if running_type == "katakana":
            await update.message.reply_text("The katakana quiz is already running. Stop it before starting hiragana.")
        else:
            await update.message.reply_text(conversation.quizAlreadyStrated, parse_mode="MarkdownV2")
        return

    context.chat_data["quiz_running"] = True
    context.chat_data["quiz_type"] = "hiragana"
    context.chat_data["current_question_id"] = -1

    chat_id = update.effective_chat.id
    context.job_queue.run_once(ask_question, when=0, chat_id=chat_id)
    await update.message.reply_text(conversation.quizStarted, parse_mode="MarkdownV2")


async def start_katakana_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cooldown = 60*1.52
    last_stopped = context.chat_data.get("last_quiz_stop_time", 0)
    elapsed = time.time() - last_stopped
    conversation.loadResponse(random_number_conversation())
    if elapsed < cooldown:
        await update.message.reply_text(
            f"{conversation.cooldown} \nWait  {int(cooldown - elapsed)} seconds",
            parse_mode="MarkdownV2"
        )
        return

    if context.chat_data.get("quiz_running", False):
        running_type = context.chat_data.get("quiz_type", "")
        if running_type == "hiragana":
            await update.message.reply_text("The hiragana quiz is already running. Stop it before starting katakana.")
        else:
            await update.message.reply_text(conversation.quizAlreadyStrated, parse_mode="MarkdownV2")
        return

    context.chat_data["quiz_running"] = True
    context.chat_data["quiz_type"] = "katakana"
    context.chat_data["current_question_id"] = -1

    chat_id = update.effective_chat.id
    context.job_queue.run_once(ask_question, when=0, chat_id=chat_id)
    await update.message.reply_text(conversation.quizStarted, parse_mode="MarkdownV2")


async def stop_any_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conversation.loadResponse(random_number_conversation())

    if not context.chat_data.get("quiz_running", False):
        await update.message.reply_text(conversation.quziAlreadyStoped, parse_mode="MarkdownV2")
        return

    context.chat_data["quiz_running"] = False
    context.chat_data["quiz_type"] = None
    context.chat_data["current_question_id"] = -1
    context.chat_data["last_quiz_stop_time"] = time.time()

    await update.message.reply_text(conversation.quizStoped, parse_mode="MarkdownV2")


async def handle_quiz_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.chat_data.get("can_answer", False):
        return

    is_running = context.chat_data.get("quiz_running", False)
    if not is_running:
        return

    conversation.loadResponse(random_number_conversation())

    quiz_type = context.chat_data.get("quiz_type", "hiragana")

    timer = 60

    chat_id = update.message.chat.id
    user_answer = update.message.text.strip().lower()
    expected = context.chat_data.get("expected_answer", "").strip().lower()
    current_question_id = context.chat_data.get("current_question_id", -1)

    if context.chat_data.get("answered"):
        return

    context.chat_data["answered"] = True

    table_name = "player_hiragana_stats" if quiz_type == "hiragana" else "player_katakana_stats"
    id_column = "hiragana_id" if quiz_type == "hiragana" else "katakana_id"

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT correcto, incorrecto FROM {table_name}
        WHERE player_id = ? AND {id_column} = ?
    """, (chat_id, current_question_id))
    row = cursor.fetchone()

    if user_answer == expected:
        if row:
            cursor.execute(f"""
                UPDATE {table_name}
                SET correcto = correcto + 1
                WHERE player_id = ? AND {id_column} = ?
            """, (chat_id, current_question_id))
        else:
            cursor.execute(f"""
                INSERT INTO {table_name} (player_id, {id_column}, correcto, incorrecto)
                VALUES (?, ?, 1, 0)
            """, (chat_id, current_question_id))
        await update.message.reply_text(conversation.correct, parse_mode="MarkdownV2")
    else:
        if row:
            cursor.execute(f"""
                UPDATE {table_name}
                SET incorrecto = incorrecto + 1
                WHERE player_id = ? AND {id_column} = ?
            """, (chat_id, current_question_id))
        else:
            cursor.execute(f"""
                INSERT INTO {table_name} (player_id, {id_column}, correcto, incorrecto)
                VALUES (?, ?, 0, 1)
            """, (chat_id, current_question_id))
        await update.message.reply_text(f"{conversation.incorrect}  \n \nAnswer: {expected}", parse_mode="MarkdownV2")

    conn.commit()
    conn.close()

    if is_running:
        job = context.job_queue.run_once(
            ask_question, when=timer, chat_id=chat_id)
        context.chat_data["current_job"] = job


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("starthiragana", start_hiragana_quiz))
    app.add_handler(CommandHandler("startkatakana", start_katakana_quiz))
    app.add_handler(CommandHandler("stopquiz", stop_any_quiz))
    app.add_handler(CommandHandler(
        "proggreshiraganaglobal", proggresHiragana_command))
    app.add_handler(CommandHandler(
        "proggreskatakanaglobal", proggresKatakana_command))
    app.add_handler(CommandHandler("sendpic", send_image_command))

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("proggreshiraganaid", proggresHiraganaID_start),
            CommandHandler("proggreskatakanaid", proggresKatakanaID_start),
        ],
        states={
            ASKING_CHAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_progress_response)],
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler)
    # Quiz response handler (must be before general message handler)
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_quiz_response))

    # Mesaggers
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # error
    app.add_error_handler(error)

    app.run_polling(poll_interval=3)
