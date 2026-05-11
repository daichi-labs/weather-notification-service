import json
import urllib.request
import urllib.error
import os

from datetime import datetime, timedelta, timezone


def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['LINE_CHANNEL_ACCESS_TOKEN']}"
    }

    user_ids = os.environ["LINE_USER_IDS"].split(",")

    for user_id in user_ids:
        body = {
            "to": user_id.strip(),
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        with urllib.request.urlopen(req) as response:
            response.read()


def lambda_handler(event, context):
    api_key = os.environ["API_KEY"]
    city = "Tokyo,jp"

    JST = timezone(timedelta(hours=9))
    today_jst = datetime.now(JST).date()

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={api_key}&lang=ja&units=metric"
    )

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        rain_times = []
        temps = []

        for item in data["list"]:
            forecast_time_utc = datetime.fromtimestamp(
                item["dt"],
                timezone.utc
            )
            forecast_time_jst = forecast_time_utc.astimezone(JST)

            if forecast_time_jst.date() != today_jst:
                continue

            weather_main = item["weather"][0]["main"]
            temp = item["main"]["temp"]

            temps.append(temp)

            if weather_main == "Rain":
                rain_times.append(forecast_time_jst)

        max_temp = max(temps)
        min_temp = min(temps)

        if not rain_times:
            message = (
                "今日は雨の予報はなさそうです☀\n\n"
                f"最高気温: {max_temp:.1f}℃\n"
                f"最低気温: {min_temp:.1f}℃"
            )
        else:
            rain_ranges = []

            start = rain_times[0]
            previous = rain_times[0]

            for current in rain_times[1:]:
                if current - previous == timedelta(hours=3):
                    previous = current
                else:
                    rain_ranges.append(
                        (start, previous + timedelta(hours=3))
                    )
                    start = current
                    previous = current

            rain_ranges.append(
                (start, previous + timedelta(hours=3))
            )

            range_texts = [
                f"{start.strftime('%H:%M')}〜{end.strftime('%H:%M')}"
                for start, end in rain_ranges
            ]

            message = (
                "今日は雨が降る予報です☔\n"
                "雨の予報時間: "
                + "、".join(range_texts)
                + "\n\n"
                f"最高気温: {max_temp:.1f}℃\n"
                f"最低気温: {min_temp:.1f}℃"
            )

        send_line_message(message)

        return {
            "statusCode": 200,
            "body": message
        }

    except urllib.error.HTTPError as e:
        error_body = e.read().decode()

        return {
            "statusCode": e.code,
            "body": error_body
        }
