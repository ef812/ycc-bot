# -*- coding: utf-8 -*-
"""
YCC (Youth Contributors Club) membership registration bot.

Flow: /start -> language -> full name -> phone (native contact share) ->
school -> grade (1-11, digits only) -> photo -> certificate generated
and sent back to the member.
"""
import logging
import os
import re

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

import db
import locales
from locales import t
import certificate

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("YCC_BOT_TOKEN", "PUT-YOUR-TOKEN-HERE")
ADMIN_IDS = {int(x) for x in os.environ.get("YCC_ADMIN_IDS", "").split(",") if x.strip().isdigit()}

# Public channel username, e.g. "@ycc_official". Must include the leading "@".
# The bot must be an admin of this channel for membership checks to work.
CHANNEL_USERNAME = os.environ.get("YCC_CHANNEL_USERNAME", "").strip()
CHANNEL_LINK = f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}" if CHANNEL_USERNAME else ""

# Conversation states
LANGUAGE, CHANNEL_GATE, NAME, PHONE, SCHOOL, GRADE, PHOTO = range(7)

NOT_MEMBER_STATUSES = {"left", "kicked"}

NAME_RE = re.compile(r"^[A-Za-zʻʼ'\u0400-\u04FF\s\-]{4,80}$")
GRADE_RE = re.compile(r"^(1[01]|[1-9])$")  # 1-11 only


def lang_of(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("language", "en")


async def is_channel_member(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    """Check via Telegram's API whether user_id has joined CHANNEL_USERNAME.
    Requires the bot to be an admin of that channel. If no channel is
    configured, the gate is skipped entirely (always returns True)."""
    if not CHANNEL_USERNAME:
        return True
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status not in NOT_MEMBER_STATUSES
    except TelegramError as e:
        logger.warning("Membership check failed for %s: %s", user_id, e)
        # Fail open would let unverified users through; fail closed is safer
        # for a "must subscribe" requirement, so treat errors as not-joined.
        return False


def channel_gate_markup(lang: str) -> InlineKeyboardMarkup:
    rows = []
    if CHANNEL_LINK:
        rows.append([InlineKeyboardButton(t("join_channel_button", lang), url=CHANNEL_LINK)])
    rows.append([InlineKeyboardButton(t("check_membership_button", lang), callback_data="check_join")])
    return InlineKeyboardMarkup(rows)


async def send_channel_gate(update_or_query, context: ContextTypes.DEFAULT_TYPE, lang: str):
    text = t("join_channel_prompt", lang, channel=CHANNEL_USERNAME)
    markup = channel_gate_markup(lang)
    if hasattr(update_or_query, "message") and update_or_query.message:
        await update_or_query.message.reply_text(text, reply_markup=markup)
    else:
        await update_or_query.reply_text(text, reply_markup=markup)


# ---------------------------------------------------------------- /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    if db.is_registered(telegram_id):
        member = db.get_member(telegram_id)
        lang = member.get("language", "en")
        await update.message.reply_text(t("already_registered", lang))
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton(label, callback_data=code)]
        for code, label in locales.LANGS.items()
    ]
    await update.message.reply_text(
        t("choose_language", "en"),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return LANGUAGE


async def language_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data
    context.user_data.clear()
    context.user_data["language"] = lang

    await query.edit_message_text(text=locales.LANGS[lang])

    if await is_channel_member(context, update.effective_user.id):
        await query.message.reply_text(t("welcome", lang), parse_mode="Markdown")
        return NAME

    await send_channel_gate(query, context, lang)
    return CHANNEL_GATE


async def channel_gate_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = lang_of(context)

    if await is_channel_member(context, update.effective_user.id):
        await query.message.reply_text(t("welcome", lang), parse_mode="Markdown")
        return NAME

    await query.message.reply_text(t("still_not_joined", lang), reply_markup=channel_gate_markup(lang))
    return CHANNEL_GATE


async def require_channel_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Auto re-check used at every later registration step. Returns True if
    the user is still (or newly) a member and the caller should proceed;
    otherwise sends the rejoin prompt and returns False."""
    lang = lang_of(context)
    if await is_channel_member(context, update.effective_user.id):
        return True
    await update.message.reply_text(
        t("left_channel_mid_registration", lang, channel=CHANNEL_USERNAME),
        reply_markup=channel_gate_markup(lang),
    )
    return False


# ---------------------------------------------------------------- name
async def name_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = lang_of(context)
    if not await require_channel_membership(update, context):
        return CHANNEL_GATE
    text = update.message.text.strip()
    if not NAME_RE.match(text) or len(text.split()) < 2:
        await update.message.reply_text(t("ask_name_again", lang))
        return NAME

    context.user_data["full_name"] = " ".join(w.capitalize() for w in text.split())

    contact_button = KeyboardButton(
        t("share_contact_button", lang), request_contact=True
    )
    markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(t("ask_phone", lang), reply_markup=markup)
    return PHONE


# ---------------------------------------------------------------- phone
async def phone_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = lang_of(context)
    if not await require_channel_membership(update, context):
        return CHANNEL_GATE
    contact = update.message.contact
    if not contact or contact.user_id != update.effective_user.id:
        await update.message.reply_text(t("ask_phone_again", lang))
        return PHONE

    context.user_data["phone"] = contact.phone_number
    await update.message.reply_text(t("ask_school", lang), reply_markup=ReplyKeyboardRemove())
    return SCHOOL


# ---------------------------------------------------------------- school
async def school_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = lang_of(context)
    if not await require_channel_membership(update, context):
        return CHANNEL_GATE
    text = update.message.text.strip()
    if len(text) < 3:
        await update.message.reply_text(t("ask_school_again", lang))
        return SCHOOL

    context.user_data["school"] = text
    await update.message.reply_text(t("ask_grade", lang), parse_mode="Markdown")
    return GRADE


# ---------------------------------------------------------------- grade
async def grade_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = lang_of(context)
    if not await require_channel_membership(update, context):
        return CHANNEL_GATE
    text = update.message.text.strip()
    if not GRADE_RE.match(text):
        await update.message.reply_text(t("ask_grade_again", lang))
        return GRADE

    context.user_data["grade"] = int(text)
    await update.message.reply_text(t("ask_photo", lang))
    return PHOTO


# ---------------------------------------------------------------- photo
async def photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = lang_of(context)
    if not await require_channel_membership(update, context):
        return CHANNEL_GATE
    if not update.message.photo:
        await update.message.reply_text(t("ask_photo_again", lang))
        return PHOTO

    photo_file_id = update.message.photo[-1].file_id
    context.user_data["photo_file_id"] = photo_file_id

    await update.message.reply_text(t("generating", lang))

    telegram_file = await context.bot.get_file(photo_file_id)
    photo_bytes = await telegram_file.download_as_bytearray()

    full_name = context.user_data["full_name"]
    school = context.user_data["school"]
    grade = context.user_data["grade"]
    phone = context.user_data["phone"]
    telegram_id = update.effective_user.id

    cert_bytes = certificate.generate_certificate(
        full_name=full_name, school=school, grade=grade, photo_bytes=bytes(photo_bytes)
    )

    db.add_member(
        telegram_id=telegram_id,
        full_name=full_name,
        phone=phone,
        school=school,
        grade=grade,
        photo_file_id=photo_file_id,
        language=lang,
    )

    caption = t("done_caption", lang, name=full_name)
    await update.message.reply_photo(
        photo=cert_bytes, caption=caption, parse_mode="Markdown"
    )

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_photo(
                chat_id=admin_id,
                photo=cert_bytes,
                caption=(
                    f"🆕 New member: {full_name}\n"
                    f"Phone: {phone}\nSchool: {school}\nGrade: {grade}\n"
                    f"Telegram ID: {telegram_id}\nLanguage: {lang}"
                ),
            )
        except Exception as e:
            logger.warning("Failed to notify admin %s: %s", admin_id, e)

    return ConversationHandler.END


# ---------------------------------------------------------------- /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = lang_of(context)
    await update.message.reply_text(t("cancelled", lang), reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


# ---------------------------------------------------------------- /mycertificate
async def my_certificate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    member = db.get_member(telegram_id)
    if not member:
        await update.message.reply_text(t("not_registered", "en"))
        return

    lang = member.get("language", "en")
    telegram_file = await context.bot.get_file(member["photo_file_id"])
    photo_bytes = await telegram_file.download_as_bytearray()

    cert_bytes = certificate.generate_certificate(
        full_name=member["full_name"],
        school=member["school"],
        grade=member["grade"],
        photo_bytes=bytes(photo_bytes),
    )
    caption = t("done_caption", lang, name=member["full_name"])
    await update.message.reply_photo(photo=cert_bytes, caption=caption, parse_mode="Markdown")


# ---------------------------------------------------------------- Admin commands
def is_admin(update: Update) -> bool:
    return update.effective_user.id in ADMIN_IDS


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    count = db.count_members()
    await update.message.reply_text(f"📊 Total registered YCC members: {count}")


async def admin_export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    csv_file = db.export_csv()
    await update.message.reply_document(document=csv_file, filename="ycc_members.csv")


async def admin_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    if not context.args:
        await update.message.reply_text("Usage: /delete <telegram_id>")
        return
    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Please provide a numeric telegram_id.")
        return
    ok = db.delete_member(target_id)
    await update.message.reply_text(
        "✅ Member deleted." if ok else "⚠️ No member found with that ID."
    )


def build_app() -> Application:
    db.init_db()
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [CallbackQueryHandler(language_chosen)],
            CHANNEL_GATE: [CallbackQueryHandler(channel_gate_check, pattern="^check_join$")],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_received)],
            PHONE: [MessageHandler(filters.CONTACT, phone_received)],
            SCHOOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, school_received)],
            GRADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, grade_received)],
            PHOTO: [MessageHandler(filters.PHOTO, photo_received)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("mycertificate", my_certificate))
    application.add_handler(CommandHandler("stats", admin_stats))
    application.add_handler(CommandHandler("export", admin_export))
    application.add_handler(CommandHandler("delete", admin_delete))

    return application


if __name__ == "__main__":
    app = build_app()
    logger.info("YCC bot starting (polling mode)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
