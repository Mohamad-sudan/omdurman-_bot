import os
import telebot
from urllib.parse import urlparse, parse_qs, unquote

TOKEN = os.environ.get("BOT_TOKEN", "8383555483:AAHdWmuQlfKKXTiOAqn0Q2tY0IfSnNyNRqg")
bot = telebot.TeleBot(TOKEN)

def unwrap(url):
    if "l.facebook.com/l.php" in url:
        qs = parse_qs(urlparse(url).query)
        if "u" in qs:
            return unquote(qs["u"][0])
    return url

def scan_logic(url):
    real = unwrap(url)
    domain = urlparse(real if "://" in real else "https://"+real).netloc.lower()
    full = real.lower()
    score = 100
    reasons = []
    if any(x in domain for x in [".xyz",".tk",".ml",".live",".top",".buzz",".sbs"]):
        score-=60; reasons.append("❌ دومين رخيص مؤقت")
    if "amazonaws.com" in domain and any(k in full for k in ["helm","fhalmc","win","prize","face","free"]):
        score-=70; reasons.append("❌ احتيال داخل Amazon S3")
    if "oghxf" in domain or "fhalmc" in domain:
        score-=50; reasons.append("❌ اسم عشوائي احتيالي")
    if "drr.ac" in domain or "gov.sd" in domain:
        score+=10; reasons.append("✅ دومين موثوق")

    if score>100: score=100
    if score<0: score=0

    if score >= 80:
        return f"🔍 {domain}\n✅ آمن {score}%\n" + "\n".join(reasons)
    elif score >=50:
        return f"🔍 {domain}\n⚠️ مشبوه {score}%\n" + "\n".join(reasons)
    else:
        return f"🔍 {domain}\n❌ احتيال مؤكد {score}% اوعى تفتحو!\n" + "\n".join(reasons)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "أهلا يا زول أم درمان! 🤗\nأنا شغال 24 ساعة هسع!\nأرسل أي رابط!")

@bot.message_handler(func=lambda m: True)
def check(m):
    if "." in m.text:
        bot.reply_to(m, scan_logic(m.text))
    else:
        bot.reply_to(m, "أرسل رابط!")

print("البوت شغال في السيرفر...")
bot.infinity_polling()
