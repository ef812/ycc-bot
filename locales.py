# -*- coding: utf-8 -*-
"""All user-facing bot text, in English, Russian and Uzbek (Latin)."""

LANGS = {
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
    "uz": "🇺🇿 O'zbekcha",
}

TEXT = {
    "choose_language": {
        "en": "Please choose your language:",
        "ru": "Пожалуйста, выберите язык:",
        "uz": "Iltimos, tilni tanlang:",
    },
    "welcome": {
        "en": (
            "👋 Welcome to *Youth Contributors Club (YCC)*!\n\n"
            "This registration is only for members living in our city.\n"
            "Let's get you registered. First, what is your *full name*?\n"
            "(Example: Maxmudov Ozodbek)"
        ),
        "ru": (
            "👋 Добро пожаловать в *Youth Contributors Club (YCC)*!\n\n"
            "Регистрация доступна только для жителей нашего города.\n"
            "Начнём регистрацию. Как вас *полностью зовут*?\n"
            "(Например: Maxmudov Ozodbek)"
        ),
        "uz": (
            "👋 *Youth Contributors Club (YCC)* ga xush kelibsiz!\n\n"
            "Ro'yxatdan o'tish faqat shahrimiz aholisi uchun.\n"
            "Keling, ro'yxatdan o'tamiz. *To'liq ismingiz* nima?\n"
            "(Masalan: Maxmudov Ozodbek)"
        ),
    },
    "ask_name_again": {
        "en": "Please enter a valid full name (letters only, at least 2 words).",
        "ru": "Пожалуйста, введите корректное полное имя (только буквы, минимум 2 слова).",
        "uz": "Iltimos, to'g'ri to'liq ism kiriting (faqat harflar, kamida 2 ta so'z).",
    },
    "ask_phone": {
        "en": "📱 Now, please share your phone number using the button below.",
        "ru": "📱 Теперь, пожалуйста, поделитесь номером телефона с помощью кнопки ниже.",
        "uz": "📱 Endi, quyidagi tugma orqali telefon raqamingizni yuboring.",
    },
    "share_contact_button": {
        "en": "📞 Share my phone number",
        "ru": "📞 Поделиться номером телефона",
        "uz": "📞 Telefon raqamimni yuborish",
    },
    "ask_phone_again": {
        "en": "Please use the button below to share your phone number (don't type it manually).",
        "ru": "Пожалуйста, используйте кнопку ниже, чтобы поделиться номером (не вводите вручную).",
        "uz": "Iltimos, telefon raqamingizni yuborish uchun quyidagi tugmadan foydalaning (qo'lda yozmang).",
    },
    "ask_school": {
        "en": "🏫 Great! What is the name of your school?",
        "ru": "🏫 Отлично! Как называется ваша школа?",
        "uz": "🏫 Ajoyib! Maktabingiz nomi nima?",
    },
    "ask_school_again": {
        "en": "Please enter a valid school name.",
        "ru": "Пожалуйста, введите корректное название школы.",
        "uz": "Iltimos, maktab nomini to'g'ri kiriting.",
    },
    "ask_grade": {
        "en": "🎓 Which grade are you in? Please type *only the number* (1-11).",
        "ru": "🎓 В каком вы классе? Введите *только число* (1-11).",
        "uz": "🎓 Nechinchi sinfda o'qiysiz? Iltimos, *faqat raqam* kiriting (1-11).",
    },
    "ask_grade_again": {
        "en": "⚠️ Please type only a number between 1 and 11 (no letters, no other symbols).",
        "ru": "⚠️ Пожалуйста, введите только число от 1 до 11 (без букв и других символов).",
        "uz": "⚠️ Iltimos, faqat 1 dan 11 gacha bo'lgan raqam kiriting (harflarsiz, boshqa belgilarsiz).",
    },
    "ask_photo": {
        "en": "📸 Almost done! Please send a clear photo of your face (for your membership certificate).",
        "ru": "📸 Почти готово! Пожалуйста, отправьте чёткое фото вашего лица (для сертификата участника).",
        "uz": "📸 Deyarli tugadi! Iltimos, yuzingizning aniq fotosuratini yuboring (a'zolik sertifikati uchun).",
    },
    "ask_photo_again": {
        "en": "Please send an actual photo (as an image, not a file/document).",
        "ru": "Пожалуйста, отправьте настоящее фото (как изображение, а не файл/документ).",
        "uz": "Iltimos, haqiqiy fotosurat yuboring (rasm sifatida, fayl/hujjat emas).",
    },
    "generating": {
        "en": "⏳ Generating your official YCC membership certificate...",
        "ru": "⏳ Формируем ваш официальный сертификат участника YCC...",
        "uz": "⏳ Sizning rasmiy YCC a'zolik sertifikatingiz tayyorlanmoqda...",
    },
    "done_caption": {
        "en": (
            "🎉 Congratulations, {name}! You are now officially a member of "
            "*Youth Contributors Club (YCC)*.\n\nWelcome aboard! 🚀"
        ),
        "ru": (
            "🎉 Поздравляем, {name}! Вы официально стали участником "
            "*Youth Contributors Club (YCC)*.\n\nДобро пожаловать! 🚀"
        ),
        "uz": (
            "🎉 Tabriklaymiz, {name}! Siz endi rasman "
            "*Youth Contributors Club (YCC)* a'zosisiz.\n\nXush kelibsiz! 🚀"
        ),
    },
    "already_registered": {
        "en": "✅ You are already registered as a YCC member. Use /mycertificate to get your certificate again.",
        "ru": "✅ Вы уже зарегистрированы как участник YCC. Используйте /mycertificate, чтобы получить сертификат снова.",
        "uz": "✅ Siz allaqachon YCC a'zosi sifatida ro'yxatdan o'tgansiz. Sertifikatni qayta olish uchun /mycertificate dan foydalaning.",
    },
    "cancelled": {
        "en": "Registration cancelled. Send /start to begin again.",
        "ru": "Регистрация отменена. Отправьте /start, чтобы начать заново.",
        "uz": "Ro'yxatdan o'tish bekor qilindi. Qaytadan boshlash uchun /start yuboring.",
    },
    "not_registered": {
        "en": "You are not registered yet. Send /start to register.",
        "ru": "Вы ещё не зарегистрированы. Отправьте /start для регистрации.",
        "uz": "Siz hali ro'yxatdan o'tmagansiz. Ro'yxatdan o'tish uchun /start yuboring.",
    },
    "join_channel_prompt": {
        "en": (
            "📢 Before registering, please join our official channel:\n{channel}\n\n"
            "Once you've joined, tap the button below."
        ),
        "ru": (
            "📢 Прежде чем зарегистрироваться, пожалуйста, подпишитесь на наш "
            "официальный канал:\n{channel}\n\n"
            "После подписки нажмите на кнопку ниже."
        ),
        "uz": (
            "📢 Ro'yxatdan o'tishdan oldin, iltimos, rasmiy kanalimizga a'zo bo'ling:\n"
            "{channel}\n\nA'zo bo'lgach, quyidagi tugmani bosing."
        ),
    },
    "join_channel_button": {
        "en": "🔗 Open channel",
        "ru": "🔗 Открыть канал",
        "uz": "🔗 Kanalni ochish",
    },
    "check_membership_button": {
        "en": "✅ I've joined",
        "ru": "✅ Я подписался",
        "uz": "✅ A'zo bo'ldim",
    },
    "still_not_joined": {
        "en": "❌ You haven't joined the channel yet. Please join, then tap the button again.",
        "ru": "❌ Вы ещё не подписались на канал. Пожалуйста, подпишитесь и нажмите кнопку снова.",
        "uz": "❌ Siz hali kanalga a'zo bo'lmagansiz. Iltimos, a'zo bo'ling va tugmani qayta bosing.",
    },
    "left_channel_mid_registration": {
        "en": (
            "⚠️ It looks like you've left our channel. Please rejoin to continue "
            "your registration:\n{channel}"
        ),
        "ru": (
            "⚠️ Похоже, вы покинули наш канал. Пожалуйста, подпишитесь снова, чтобы "
            "продолжить регистрацию:\n{channel}"
        ),
        "uz": (
            "⚠️ Siz kanaldan chiqib ketgan ko'rinasiz. Ro'yxatdan o'tishni davom "
            "ettirish uchun qaytadan a'zo bo'ling:\n{channel}"
        ),
    },
}


def t(key: str, lang: str, **kwargs) -> str:
    """Fetch localized text, defaulting to English, and format with kwargs."""
    entry = TEXT.get(key, {})
    s = entry.get(lang) or entry.get("en") or key
    if kwargs:
        s = s.format(**kwargs)
    return s
