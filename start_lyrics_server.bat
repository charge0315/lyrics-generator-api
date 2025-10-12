@echo off
chcp 65001 >nul
REM Lyrics API Server + ngrok startup script
REM
REM 使い方:
REM   1. venv\Scripts\activate を実行して仮想環境に入る
REM   2. このスクリプトを実行: start_lyrics_server.bat
REM
REM 必要な環境:
REM   - Python 3.x がインストール済み
REM   - GENIUS_API_KEY が環境変数に設定済み（オプション）
REM
REM このスクリプトは以下を自動実行します:
REM   - 仮想環境が無ければ作成
REM   - PowerShell実行ポリシーの設定
REM   - 必要なパッケージのインストール（uvicorn, fastapi, lyricsgenius, pyngrok）
REM   - FastAPIサーバーとngrokの起動

echo ===================================
echo Lyrics API Server + ngrok startup
echo ===================================
echo.

REM 仮想環境のアクティベート確認
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] venv が見つかりません。仮想環境を作成します...

    REM PowerShellの実行ポリシーを設定
    echo [INFO] PowerShellの実行ポリシーを設定します...
    powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

    REM 仮想環境を作成
    echo [INFO] 仮想環境を作成中...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] 仮想環境の作成に失敗しました。
        pause
        exit /b 1
    )
    echo [INFO] 仮想環境の作成が完了しました。
)

REM 仮想環境をアクティベート
call venv\Scripts\activate.bat

REM 依存チェック
python -c "import uvicorn, fastapi, lyricsgenius, pyngrok" 2>nul
if errorlevel 1 (
    echo [INFO] 必要なライブラリをインストールします...
    pip install uvicorn fastapi lyricsgenius pyngrok
    if errorlevel 1 (
        echo [ERROR] ライブラリのインストールに失敗しました。
        pause
        exit /b 1
    )
    echo [INFO] ライブラリのインストールが完了しました。
)

echo [INFO] FastAPI サーバーを起動します（ポート8000）...
start "Lyrics API Server" cmd /k "chcp 65001 >nul && venv\Scripts\activate.bat && uvicorn scripts.lyrics_api:app --reload --port 8000"

REM サーバー起動待機
timeout /t 3 /nobreak >nul

echo [INFO] ngrok でポート8000を公開します...
start "ngrok" cmd /k "chcp 65001 >nul && venv\Scripts\activate.bat && python scripts\start_ngrok.py"

echo.
echo ===================================
echo 起動完了！
echo ===================================
echo.
echo FastAPI: http://localhost:8000
echo ngrok URL: 新しいウィンドウで確認してください
echo.
echo Ctrl+C で各ウィンドウを終了できます
echo.
pause
