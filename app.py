from flask import Flask
app = Flask(__name__)

from flask import request, abort
#from flask_sqlalchemy import SQLAlchemy
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import http.client, json

line_bot_api = LineBotApi('P4HnvzqEDlH2rcmKEK+PV5Ogl3wIg5nZdXo02O43SQ9cqKDNGt8A9VvEfmWvKeZp506huN2PyVIO2RSYnu5iaAIhJmB/6xO0juJtpH0Zx4sJNPS78R4DiOG4POf3UmVI9chGmdxBjvsmB9xdT+gMSQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5b7532d9f8305a3a64c427412964be4a')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

host = 'd0636.azurewebsites.net'  #主機
endpoint_key = "9d153e46-f529-47c3-9d5a-dae6e5c2c5bb"  #授權碼
kb = "f8d5ba54-c2d9-44eb-a0dd-09e5b7a29811"  #GUID碼
method = "/qnamaker/knowledgebases/" + kb + "/generateAnswer"

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://管理者名稱:管理者密碼@127.0.0.1:5432/NTUHQA'
#db = SQLAlchemy(app)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '@使用說明':
        sendUse(event)

    else:
        sendQnA(event, mtext)

def sendQnA(event, mtext):  #QnA
    question = {
        'question': mtext,
    }
    content = json.dumps(question)
    headers = {
        'Authorization': 'EndpointKey ' + endpoint_key,
        'Content-Type': 'application/json',
        'Content-Length': len(content)
    }
    conn = http.client.HTTPSConnection(host)
    conn.request ("POST", method, content, headers)
    response = conn.getresponse ()
    result = json.loads(response.read())
    result1 = result['answers'][0]['answer']
  
    if 'No good match' in result1:
        text1 = '很抱歉，資料庫中無適當解答！請再輸入問題或來電由專人為您服務，電話：(06)216-0216，國稅與地方稅免付費電話：0800-000-321（限辦公時間提供服務）'
        #將沒有解答的問題寫入資料庫

    else:
        result2 = result1  #移除「A：」
        text1 = result2
    message = TextSendMessage(
        text = text1
    )
    line_bot_api.reply_message(event.reply_token,message)

if __name__ == '__main__':
    app.run()
