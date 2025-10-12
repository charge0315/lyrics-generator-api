#!/bin/bash
# Lyrics API Server + ngrok startup script (Linux/Mac)
#
# 使い方:
#   chmod +x start_lyrics_server.sh
#   ./start_lyrics_server.sh
#
# 必要な環境:
#   - venv に uvicorn, fastapi, lyricsgenius がインストール済み
#   - ngrok がインストール済み
#   - GENIUS_API_KEY が環境変数に設定済み（オプション）

echo "==================================="
echo "Lyrics API Server + ngrok startup"
echo "==================================="
echo ""

# 仮想環境のアクティベート確認
if [ ! -f "venv/bin/activate" ]; then
    echo "[ERROR] venv が見つかりません。先に仮想環境を作成してください。"
    echo "  python -m venv venv"
    exit 1
fi

# 仮想環境をアクティベート
source venv/bin/activate

# 依存チェック
python -c "import uvicorn, fastapi, lyricsgenius" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] 必要なライブラリがインストールされていません。"
    echo "  pip install uvicorn fastapi lyricsgenius"
    exit 1
fi

# ngrokチェック
which ngrok >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[ERROR] ngrok が見つかりません。パスに追加するか、インストールしてください。"
    exit 1
fi

echo "[INFO] FastAPI サーバーを起動します（ポート8000）..."
uvicorn scripts.lyrics_api:app --reload --port 8000 &
SERVER_PID=$!

# サーバー起動待機
sleep 3

echo "[INFO] ngrok でポート8000を公開します..."
ngrok http 8000 &
NGROK_PID=$!

echo ""
echo "==================================="
echo "起動完了！"
echo "==================================="
echo ""
echo "FastAPI: http://localhost:8000"
echo "ngrok URL: http://localhost:4040 で確認してください"
echo ""
echo "Ctrl+C で終了します"
echo ""

# トラップで終了時にプロセスをクリーンアップ
trap "kill $SERVER_PID $NGROK_PID 2>/dev/null; exit" INT TERM

# 待機
wait
