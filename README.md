# switchbot_thermal_getter
Switchbotの温度を取得するFunction

## 開発

vscodeで `launch local function` を起動した状態で↓で動作確認。
```bash
curl "http://localhost:8080/?device_id={デバイスID}"
```

テストはvscodeのTestingでpytestを呼び出して実行。

## デプロイ
settings.pyで指定されている環境変数を `.env.prod.yaml` として用意した上で↓を実行。

```bash
gcloud functions deploy get-switchbot-thermal \
    --no-allow-unauthenticated \
    --ingress-settings=internal-only \
    --gen2 \
    --entry-point=main \
    --region=us-central1 \
    --runtime=python312 \
    --cpu=.083 \
    --memory=128Mi \
    --min-instances=0 \
    --max-instances=3 \
    --env-vars-file=.env.prod.yaml \
    --timeout=1m \
    --trigger-http \
    --concurrency=1
```
