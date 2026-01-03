import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from predictor import generate_prediction, get_past_results

# Load environment variables
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Halo Bosku! Selamat datang di **AI PREDIKTOR Cuaca ⚽**\n\n"
        "Gunakan bot ini untuk melihat prediksi skor jitu ala orang dalam! 🤫\n\n"
        "🔥 **Fitur Baru**: Ketik `/bukti` untuk lihat riwayat jackpot kita!\n\n"
        "Cara pakai:\n"
        "Ketik: `TeamA vs TeamB`\n"
        "Contoh: `Manchester United vs Liverpool`\n\n"
        "Gas terus jangan kasih kendor! 🔥💸"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text, parse_mode='Markdown')

async def bukti_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results = get_past_results()
    message = "💰 **BUKTI JP / WIN STREAK (Last 10 Matches)** 💰\n\n"
    
    for item in results:
        message += f"🏆 {item['match']} | Skor: {item['api_score']}\n"
        message += f"🎯 Tips: {item['tip']} -> {item['status']}\n\n"
        
    message += "🔥 **Status: LUNAS DIBAYAR BANDAR** 🔥\n"
    message += "Jangan ragu bos, data berbicara! 💸"
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')

async def predict_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    if "vs" not in query.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="⚠️ Format salah bos! Pake format: `TeamA vs TeamB` biar gacor!"
        )
        return

    data = generate_prediction(query)
    
    if not data:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Gagal baca tim bos, coba lagi!")
        return

    # Teaser Message (Prediksi Setengah Matang)
    message = (
        f"🏆 **AI PREDIKTOR Cuaca ⚽** 🏆\n"
        f"📅 Match: {data['team_a']} 🆚 {data['team_b']}\n\n"
        f"☁️ **Kondisi Cuaca ⚽**: {data['cuaca']}\n"
        f"📊 **Statistik Orang Dalam**:\n"
        f"   • {data['team_a']} Win Rate: {data['win_prob_a']}%\n"
        f"   • Ball Possession: {data['possession_a']}% - {data['possession_b']}%\n\n"
        f"🎯 **PREDIKSI SKOR AKHIR**:\n"
        f"   🔥 {data['team_a']} {data['score_a']} - {data['score_b']} {data['team_b']} 🔥\n\n"
        f"💰 **Confidence**: {data['confidence']}%\n"
        f"🎲 **Bet Advice**: {'Over' if data['total_goals'] > 2 else 'Under'} 2.5 Goals\n\n"
        f"⚠️ _Disclaimer: Ini cuma prediksi robot ya bos, tetap dior (do your own research). Salam Profit!_ 💸💎"
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')

if __name__ == '__main__':
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN or TOKEN == "YOUR_TOKEN_HERE":
        print("❌ Error: Token belum diisi di file .env!")
        exit(1)
        
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('bukti', bukti_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), predict_handler))
    
    print("✅ Bot AI PREDIKTOR Cuaca ⚽ is running...")
    application.run_polling()
