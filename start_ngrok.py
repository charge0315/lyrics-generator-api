#!/usr/bin/env python
"""ngrokを起動してポート8000を公開するスクリプト"""
from pyngrok import ngrok

# ポート8000へのトンネルを作成
tunnel = ngrok.connect(8000)
print(f"\nngrok tunnel created: {tunnel.public_url}")
print("Press Ctrl+C to stop ngrok\n")

try:
    # トンネルを維持
    ngrok.get_ngrok_process().proc.wait()
except KeyboardInterrupt:
    print("\nShutting down ngrok...")
    ngrok.kill()
