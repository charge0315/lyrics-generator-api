# Lyrics Generator API 🎵

Google Colab向けローカル歌詞取得APIサーバー

## 🎯 概要

このAPIサーバーは、Google ColabからローカルのLyrics APIを使用して歌詞を取得するためのFastAPIベースのサーバーです。ngrokを使用してローカルサーバーを外部に公開し、Colab環境から安全に歌詞データを取得できます。

## 🚀 クイックスタート

### Windows

```bash
start_lyrics_server.bat
```

### Linux/Mac

```bash
chmod +x start_lyrics_server.sh
./start_lyrics_server.sh
```

これにより、以下が自動的に実行されます:

- FastAPI サーバーが `http://localhost:8000` で起動
- ngrok が起動して外部公開 URL が生成される

## 📋 前提条件

- Python 3.8 以上
- ngrok がインストール済み
- GENIUS_API_KEY が取得済み

## 🔧 セットアップ手順

### 1. 依存ライブラリのインストール

仮想環境をアクティベートして、必要なライブラリをインストールします。

**Windows:**

```bash
venv\Scripts\activate
pip install uvicorn fastapi lyricsgenius
```

**Linux/Mac:**

```bash
source venv/bin/activate
pip install uvicorn fastapi lyricsgenius
```

### 2. 環境変数の設定（オプション）

GENIUS_API_KEY を環境変数として設定する場合:

**Windows:**

```bash
set GENIUS_API_KEY=your_genius_api_key_here
```

**Linux/Mac:**

```bash
export GENIUS_API_KEY=your_genius_api_key_here
```

> **注意**: 環境変数を設定しない場合は、`fetch_lyrics.py` 内のハードコーディングされた API キーが使用されます。

### 3. 手動起動する方法

#### ターミナル1: FastAPI サーバー

```bash
venv\Scripts\activate  # Windows
# または
source venv/bin/activate  # Linux/Mac

uvicorn lyrics_api:app --reload --port 8000
```

#### ターミナル2: ngrok

```bash
ngrok http 8000
```

### 4. ngrok の公開 URL を確認

ngrok のターミナルまたは [http://localhost:4040](http://localhost:4040) にアクセスして、公開 URL を確認します。

例: `https://xxxx-xx-xx-xxx-xxx.ngrok-free.app`

### 5. Google Colab での設定

Colab ノートブックの「ローカル Lyrics API 設定」セルで以下を設定します:

```python
USE_LOCAL_LYRICS_API = True  # True に変更
LYRICS_API_URL = "https://xxxx-xx-xx-xxx-xxx.ngrok-free.app"  # ngrok の URL を貼り付け
```

## 📡 API エンドポイント

### ヘルスチェック

```text
GET /healthz
```

レスポンス:

```json
{"status": "ok"}
```

### 歌詞取得（POST）

```text
POST /api/v1/lyrics
Content-Type: application/json

{
  "artist": "Adele",
  "title": "Hello",
  "save": true,
  "overwrite": false
}
```

レスポンス:

```json
{
  "artist": "Adele",
  "title": "Hello",
  "lyrics": "Hello, it's me...",
  "from_cache": false,
  "saved_path": "lyrics/Adele_Hello.txt"
}
```

### 歌詞取得（GET - キャッシュのみ）

```text
GET /api/v1/lyrics?artist=Adele&title=Hello
```

## 🔄 動作フロー

1. **Colab** → ngrok URL に POST リクエスト
2. **ローカルサーバー** → 既存キャッシュをチェック
3. キャッシュがない場合 → **Genius API** に問い合わせ
4. 歌詞を取得 → `lyrics/` ディレクトリに保存（`save=true` の場合）
5. **Colab** にレスポンスを返す

## 🛠️ トラブルシューティング

### ngrok の URL が見つからない

- ngrok のターミナルウィンドウを確認
- [http://localhost:4040](http://localhost:4040) にアクセスして URL を確認

### API 接続エラー

- ファイアウォールで 8000 番ポートが許可されているか確認
- ngrok の無料プランの制限に注意（セッション時間制限あり）

### 歌詞が取得できない

- GENIUS_API_KEY が正しく設定されているか確認
- `fetch_lyrics.py` 内の API キーを確認
- ローカルサーバーのログを確認

## ⚠️ 注意事項

- ngrok の無料プランは一定時間でセッションが切断されます
- セッションが切れた場合は、ngrok を再起動して新しい URL を Colab に設定してください
- API キーは公開リポジトリにコミットしないように注意してください

## 📁 ファイル構成

```
lyrics-generator-api/
├── lyrics_api.py           # FastAPI メインサーバー
├── fetch_lyrics.py         # 歌詞取得コアロジック
├── start_ngrok.py          # ngrok 起動スクリプト
├── start_lyrics_server.bat # Windows 自動起動スクリプト
├── start_lyrics_server.sh  # Linux/Mac 自動起動スクリプト
└── README.md              # このファイル
```

## 🔗 関連プロジェクト

- [audio-dataset-forge](https://github.com/charge0315/audio-dataset-forge) - MusicGen学習用音楽データセット生成ツール