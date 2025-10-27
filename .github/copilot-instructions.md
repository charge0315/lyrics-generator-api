# Copilot Instructions for AI Agents

## 概要
このリポジトリは Google Colab から利用するローカル歌詞取得APIサーバ（FastAPI）です。

## 主要機能・構成
- API: lyrics_api.py, fetch_lyrics.py
- 起動スクリプト: start_lyrics_server.bat, start_lyrics_server.sh, start_ngrok.py
- 主要コマンド: python -m venv, pip install -r requirements.txt, uvicorn lyrics_api:app --reload --port 8000

## 開発・実行コマンド
- 仮想環境作成: python -m venv venv
- 有効化: .\venv\Scripts\Activate.ps1
- 依存インストール: pip install -r requirements.txt
- サーバ起動: uvicorn lyrics_api:app --reload --port 8000
- ngrok起動: python start_ngrok.py

## 注意点・運用ルール
- Genius APIキーは環境変数で管理
- キャッシュ優先設計（lyrics/ ディレクトリ）
- 無料ngrokはセッション制限あり

---
このテンプレートは自動生成です。プロジェクト固有の注意点はREADMEも参照してください。
