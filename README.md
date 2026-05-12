# 天気通知サービス　システム概要

本サービスは、以下2つの AWS Lambda によって構成されています。

## 1. ユーザーID取得機能（line-webhook-receiver-function）
LINE公式アカウントに送信されたメッセージをもとに、
通知対象ユーザーの LINE userId を取得する機能です。

LINE公式アカウントにユーザーがメッセージを送信すると、
LINE Messaging API の Webhook 機能によって、
メッセージ情報が API Gateway に送信されます。

API Gateway 経由で Lambda を実行し、
CloudWatch Logs に出力された情報から LINE userId を取得しています。

取得した userId を
通知対象ユーザーとして Lambda の環境変数 `LINE_USER_IDS` に手動で設定しています。


## 2. 天気通知機能（weather-notification-function）

毎朝6時に、その日の天気予報を LINE に自動通知する機能です。

EventBridge に設定したスケジュール（AM6:00）で Lambda 関数を実行し、
OpenWeather API から天気情報を取得します。

取得した最高気温・最低気温・雨予報時間を整形し、
LINE Messaging API 経由で登録ユーザーへ通知しています。




## 使用技術

- AWS Lambda
- Amazon EventBridge
- Amazon API Gateway
- Amazon CloudWatch
- LINE Messaging API
- OpenWeather API
- Python

## 主な機能

- 毎朝6時に天気通知
- 雨予報時間の通知
- 最高気温 / 最低気温通知
- LINE通知
- 複数ユーザー通知

## 環境変数

- API_KEY
- LINE_CHANNEL_ACCESS_TOKEN
- LINE_USER_IDS

## システム構成図（天気通知機能）

<img width="721" height="531" alt="architecture" src="https://github.com/user-attachments/assets/0c04a685-f077-4d65-8c0f-795ff0be0b1c" />

## 今後の改善予定

- 地域登録機能
- DynamoDBによるユーザー管理
- Web UI作成
- GitHub ActionsによるCI/CD
