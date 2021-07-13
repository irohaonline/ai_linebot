"""
画像解析 Line Bot
"""

import os
import statistics
import operator
import boto3


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage
)


handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

client = boto3.client('rekognition')


def lambda_handler(event, context):
    headers = event["headers"]
    body = event["body"]

    # get X-Line-Signature header value
    signature = headers['x-line-signature']

    # handle webhook body
    handler.handle(body, signature)

    return {"statusCode": 200, "body": "OK"}


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """ TextMessage handler """
    input_text = event.message.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=input_text))


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # 送られてきた写真を一時ファイルとして保存
    message_content = line_bot_api.get_message_content(event.message.id)
    file_path = "/tmp/sent-image.jpg"
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    # Rekogintion で感情分析
    with open(file_path, 'rb') as fd:
        sent_image_binary = fd.read()
        response = client.detect_faces(Image={"Bytes": sent_image_binary}, Attributes=["ALL"])

    print(response)

    def most_confidence_emotion(emotions):
        """
        最も確信度が高い感情とその確信度を返す
        """
        max_conf = 0
        result = {}
        for e in emotions:
            if max_conf < e["Confidence"]:
                max_conf = e["Confidence"]
                result = {"emotion": e["Type"], "confidence": e["Confidence"]}
        return result #{emotion:  , cofidence:  }



    def estimate_age(agerange):
        estimated_age = (agerange["High"] + agerange["Low"]) / 2
        return estimated_age 

    def estimate_gender(gender):
        estimated_gender = {"gender": gender["Value"], "confidence": gender["Confidence"]}
        return estimated_gender

    # introduce all 
    def detect_all(result):
        emotions_ages = []
        #[{emotion:  , age:  , gender:  }...]
        for detail in result["FaceDetails"]:
            emotions_ages_elm = {"emotion": most_confidence_emotion(detail["Emotions"]), "age": estimate_age(detail["AgeRange"]), "gender": estimate_gender(detail["Gender"])}
            emotions_ages.append(emotions_ages_elm)
        return  emotions_ages

    # message = str(detect_all(response))

    emotion = (detect_all(response))[0]["emotion"]
    age = (detect_all(response))[0]["age"]
    gender = (detect_all(response))[0]["gender"]

    message = "感情: " + emotion["emotion"] + "(" + str(round(emotion["confidence"])) + "%)" + "\n" + "推定年齢: " + str(round(age)) + "\n" + "推定性別: " + gender["gender"] + "(" + str(round(gender["confidence"])) + "%)"


    # 返答
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message)
    )

    # file_path の画像を削除
    os.remove(file_path)