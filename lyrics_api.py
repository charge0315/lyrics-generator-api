"""FastAPI based Lyrics Retrieval API

エンドポイント:
  GET /healthz -> ヘルスチェック {status: ok}
  POST /api/v1/lyrics -> {artist, title, save?} を受け取り 歌詞を取得/保存
  GET /api/v1/lyrics?artist=...&title=... -> 取得済みファイルから歌詞を返却 (存在すれば)

保存仕様:
  fetch_lyrics.save_lyrics と同じく lyrics/<Artist>_<Title>.txt に UTF-8

キャッシュ戦略:
  1. まず既存ファイルがあれば読み込んで即返す
  2. 無ければ Genius API に問い合わせ fetch_lyrics.fetch_lyrics を使用
  3. save=true の場合保存 (false なら保存せずレスポンスのみ)

環境変数:
  GENIUS_API_KEY があればそれを優先 (fetch_lyrics 内のハードコード上書き)

Colab からの利用例:
  import requests
  res = requests.post(url, json={"artist": "Adele", "title": "Hello", "save": True})

起動:
  uvicorn scripts.lyrics_api:app --reload --port 8000
"""
from __future__ import annotations
import os
import pathlib
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

# 既存スクリプト関数をインポート
import fetch_lyrics as core  # type: ignore

# 環境変数 GENIUS_API_KEY があれば上書き (ランタイム差し替え用)
if os.getenv("GENIUS_API_KEY"):
    core.API_KEY = os.environ["GENIUS_API_KEY"]

app = FastAPI(title="Lyrics API", version="0.1.0")

class LyricsRequest(BaseModel):
    artist: str = Field(..., description="歌手名")
    title: str = Field(..., description="曲名")
    save: bool = Field(True, description="取得した歌詞をサーバ側保存するか")
    overwrite: bool = Field(False, description="既存ファイルがあっても再取得する")

class LyricsResponse(BaseModel):
    artist: str
    title: str
    lyrics: str
    from_cache: bool
    saved_path: Optional[str] = None

LYRICS_DIR = "lyrics"


def _build_path(artist: str, title: str) -> pathlib.Path:
    safe_artist = artist.replace("/", "-").replace(" ", "_")
    safe_title = title.replace("/", "-").replace(" ", "_")
    return pathlib.Path(LYRICS_DIR) / f"{safe_artist}_{safe_title}.txt"

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/api/v1/lyrics", response_model=LyricsResponse)
async def get_lyrics(artist: str = Query(...), title: str = Query(...)):
    path = _build_path(artist, title)
    if not path.exists():
        raise HTTPException(status_code=404, detail="lyrics not cached")
    text = path.read_text(encoding="utf-8")
    return LyricsResponse(artist=artist, title=title, lyrics=text, from_cache=True, saved_path=str(path))

@app.post("/api/v1/lyrics", response_model=LyricsResponse)
async def post_lyrics(req: LyricsRequest):
    path = _build_path(req.artist, req.title)
    if path.exists() and not req.overwrite:
        text = path.read_text(encoding="utf-8")
        return LyricsResponse(artist=req.artist, title=req.title, lyrics=text, from_cache=True, saved_path=str(path))

    client = core.build_client()
    lyrics = core.fetch_lyrics(req.artist, req.title, client)
    if lyrics is None:
        raise HTTPException(status_code=404, detail="lyrics not found")

    saved_path = None
    if req.save:
        saved_path = core.save_lyrics(req.artist, req.title, lyrics)
    return LyricsResponse(artist=req.artist, title=req.title, lyrics=lyrics, from_cache=False, saved_path=saved_path)

# 簡易トップ
@app.get("/")
async def root():
    return {"msg": "Lyrics API. POST /api/v1/lyrics {artist,title}"}
