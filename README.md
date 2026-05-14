# 天気通知サービス　システム概要

<img width="600" alt="LINE_背景" src="https://github.com/user-attachments/assets/3ccd055a-133f-4bc9-8c0b-4b9f6b6192ff" />

本サービスは、以下2つの AWS Lambda によって構成されています。

## 1. ユーザーID取得機能（line-webhook-receiver-function）

LINE公式アカウントに送信されたメッセージをもとに、
通知対象ユーザーの LINE userId を取得し、DynamoDB に登録する機能です。

ユーザーが LINE公式アカウントに「登録」とメッセージを送信すると、
LINE Messaging API の Webhook 機能によって、
メッセージ情報が API Gateway に送信されます。

API Gateway 経由で Lambda を実行し、
取得した LINE userId を DynamoDB に登録しています。



## 2. 天気通知機能（weather-notification-function）

毎朝5:30に、その日の天気予報を LINE に自動通知する機能です。

EventBridge に設定したスケジュール（AM5:30）で Lambda 関数を実行し、
OpenWeather API から天気情報を取得します。

取得した最高気温・最低気温・雨予報時間を整形し、
LINE Messaging API 経由で DynamoDB に登録されたユーザーへ通知しています。




## 使用技術

- AWS Lambda
- Amazon EventBridge
- Amazon API Gateway
- Amazon CloudWatch
- LINE Messaging API
- OpenWeather API
- Python


## 主な機能

- 毎朝5:30に天気通知
- 雨予報時間の通知
- 最高気温 / 最低気温通知
- LINE通知
- 複数ユーザー通知


## 環境変数

- API_KEY
- LINE_CHANNEL_ACCESS_TOKEN



## システム構成図（ユーザーID取得機能）

<img width="771" height="321" alt="ユーザーID取得機能_line-webhook-receiver-function_構成図 drawio" src="https://github.com/user-attachments/assets/8b528231-ec4d-46d4-9100-c98ff90685bf" />







## システム構成図（天気通知機能）

<img width="711" height="531" alt="天気通知機能_weather-notification-function_構成図 drawio" src="https://github.com/user-attachments/assets/16e4e92e-90ef-4638-bf0a-5668004e3716" />







## 工夫した点

- OpenWeather API の3時間ごとの天気予報データをもとに、雨予報時間を算出
- APIキーやアクセストークンを環境変数で管理し、コードへの直書きを回避
- Webhook を利用して LINE userId を取得
- Lambda 関数をユーザーID取得機能と天気通知機能に分割し、役割を明確化


  
## 今後の改善予定

- 地域登録機能
- ユーザ登録の自動化 → DynamoDBを用いたユーザ登録の自動化を完了
- Web UI作成
- GitHub ActionsによるCI/CD
