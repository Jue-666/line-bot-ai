from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 請貼上你的 token 跟 secret
line_bot_api = LineBotApi("【貼上你的 Channel Access Token】")
handler = WebhookHandler("【貼上你的 Channel Secret】")

def classify_item(text):
    text = text.strip()
    if text in ["寶特瓶", "鋁罐", "紙箱"]:
        return "這是可回收物！"
    elif text in ["蘋果核", "雞骨頭", "菜葉"]:
        return "這是廚餘喔～"
    elif text in ["塑膠袋", "吸管", "破布"]:
        return "這是一般垃圾。"
    else:
        return "這我不確定欸～"

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text
    reply = classify_item(user_msg)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run()
