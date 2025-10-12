"""
fetch_lyrics.py

Genius (lyricsgenius) API を用いて歌手名 + 曲名で歌詞を取得するシンプルなスクリプト。
ユーザー要望: APIキーをハードコーディング。

【重要】本番運用では API キーのハードコーディングは避け、環境変数や秘密管理を利用してください。

使い方:
  1) 依存インストール: pip install lyricsgenius
  2) コマンド例:
        python scripts/fetch_lyrics.py --artist "Adele" --title "Hello" --save
     もしくは
        python scripts/fetch_lyrics.py -a Adele -t Hello
  3) 成功すると標準出力に歌詞を表示し、--save 指定時は ./lyrics/Adele_Hello.txt に保存。

エラー処理:
  - 曲が見つからない場合は候補上位5件を表示
  - API 通信エラー時は HTTP ステータスや例外を表示
  - 429 (Rate limit) 場合は待機提案

改良アイデア (未実装):
  - キャッシュ (JSON) 化
  - 複数候補からインタラクティブ選択
  - 歌詞の言語自動判定
"""
from __future__ import annotations
import argparse
import os
import sys
import textwrap
from typing import Optional

try:
    import lyricsgenius  # type: ignore
except ImportError:  # ユーザーが未インストールの場合に案内
    print("lyricsgenius がインポートできません。先に: pip install lyricsgenius")
    raise

# ====== ハードコーディングされた API キー (ユーザーが置き換えてください) ======
API_KEY = "oi_wo2irsSBRK9NzLNfiarxChvqzcLx9mOcIf3BWUi1npRD4Yg0UkufzPKVrb9pH"  # ← Genius の個人アクセストークンをここに貼る
# =============================================================================

if API_KEY.startswith("PUT_"):
    print("[警告] API_KEY がデフォルトのままです。Genius のアクセストークンを fetch_lyrics.py 内で設定してください。", file=sys.stderr)


def build_client(timeout: int = 10, retries: int = 3) -> "lyricsgenius.Genius":
    """lyricsgenius のクライアントを構築して返す。"""
    client = lyricsgenius.Genius(
        API_KEY,
        timeout=timeout,
        retries=retries,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"],
        remove_section_headers=True,
        verbose=False,
    )
    return client


def fetch_lyrics(artist: str, title: str, client: Optional["lyricsgenius.Genius"] = None) -> Optional[str]:
    """歌手名と曲名から歌詞を取得。見つからない場合は None。

    1. search_song(title, artist) を試行
    2. 失敗したら client.search_songs(title) で候補表示 (標準エラー)
    """
    if client is None:
        client = build_client()

    try:
        song = client.search_song(title, artist)
    except Exception as e:
        print(f"[エラー] 検索リクエスト失敗: {e}", file=sys.stderr)
        return None

    if song and song.lyrics:
        return _clean_lyrics(song.lyrics)

    # 直接見つからなかったのでタイトルだけで候補検索
    try:
        res = client.search_songs(title, per_page=5)
        hits = res.get("hits", []) if isinstance(res, dict) else []
        if not hits:
            print("[情報] 候補が見つかりませんでした。", file=sys.stderr)
            return None
        print("[候補表示] 直接一致がなかったため近い候補を表示します:", file=sys.stderr)
        for i, h in enumerate(hits, 1):
            full_title = h.get("result", {}).get("full_title", "?")
            print(f"  {i}. {full_title}", file=sys.stderr)
    except Exception as e:
        print(f"[エラー] 候補取得失敗: {e}", file=sys.stderr)
    return None


def _clean_lyrics(raw: str) -> str:
    """歌詞テキストから不要な重複ヘッダや末尾の埋め込みURL等を軽く除去。"""
    lines = raw.splitlines()
    cleaned = []
    seen = set()
    for ln in lines:
        # 重複セクションや空行過多の抑制
        key = ln.strip().lower()
        if key in seen and key.startswith("[") and key.endswith("]"):
            continue
        if ln.startswith("https://") and "genius.com" in ln:
            continue
        cleaned.append(ln.rstrip())
        if key:
            seen.add(key)
    # 連続空行を1行に
    final = []
    blank = False
    for ln in cleaned:
        if ln.strip() == "":
            if blank:
                continue
            blank = True
        else:
            blank = False
        final.append(ln)
    return "\n".join(final).strip() + "\n"


def save_lyrics(artist: str, title: str, lyrics: str, out_dir: str = "lyrics") -> str:
    os.makedirs(out_dir, exist_ok=True)
    safe_artist = artist.replace("/", "-").replace(" ", "_")
    safe_title = title.replace("/", "-").replace(" ", "_")
    path = os.path.join(out_dir, f"{safe_artist}_{safe_title}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(lyrics)
    return path


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Genius API を使って歌詞を取得 (artist + title)" ,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            例:
              python scripts/fetch_lyrics.py -a Adele -t Hello --save
            """
        )
    )
    p.add_argument('-a', '--artist', required=True, help='歌手名 (例: Adele)')
    p.add_argument('-t', '--title', required=True, help='曲名 (例: Hello)')
    p.add_argument('--no-color', action='store_true', help='色付け出力を無効化')
    p.add_argument('--save', action='store_true', help='lyrics ディレクトリに保存')
    p.add_argument('--timeout', type=int, default=10, help='HTTP タイムアウト秒')
    p.add_argument('--retries', type=int, default=3, help='リトライ回数')
    return p.parse_args(argv)


def color(text: str, code: str, use_color: bool) -> str:
    if not use_color:
        return text
    return f"\033[{code}m{text}\033[0m"


def main(argv=None):
    args = parse_args(argv)
    client = build_client(timeout=args.timeout, retries=args.retries)

    lyrics = fetch_lyrics(args.artist, args.title, client)
    if lyrics is None:
        print("歌詞が取得できませんでした。", file=sys.stderr)
        return 2

    header = f"{args.artist} - {args.title}"
    print(color("=" * len(header), "36", not args.no_color))
    print(color(header, "36;1", not args.no_color))
    print(color("=" * len(header), "36", not args.no_color))
    print(lyrics)

    if args.save:
        path = save_lyrics(args.artist, args.title, lyrics)
        print(color(f"[保存済] {path}", "32", not args.no_color), file=sys.stderr)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
