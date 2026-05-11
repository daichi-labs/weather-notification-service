# weather-notification-service

AWS Lambda と LINE Messaging API を利用した天気通知サービスです。

毎朝6時に、その日の天気予報をLINEへ自動通知します。

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

## システム構成

EventBridge
↓
Lambda
↓
OpenWeather API
↓
LINE Messaging API
↓
LINE通知

## 環境変数

- API_KEY
- LINE_CHANNEL_ACCESS_TOKEN
- LINE_USER_IDS

## システム構成図（通知機能）

<img width="650" height="531" alt="architecture" src="https://github.com/user-attachments/assets/0c04a685-f077-4d65-8c0f-795ff0be0b1c" />

## 今後の改善予定

- 地域登録機能
- DynamoDBによるユーザー管理
- Web UI作成
- GitHub ActionsによるCI/CD
