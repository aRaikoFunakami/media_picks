# Media Picks

**CineBot** - 音声対応映画・TV番組レコメンデーションエージェント

Media Picksは、OpenAI Realtime APIを活用した音声対応の映画・TV番組レコメンデーションボットです。自然言語での音声入力に対して、ユーザーの好みや気分、地域、物語のテーマに基づいて最適なエンターテインメント作品をレコメンドします。

## 🎬 主な機能

### 🎤 音声対応レコメンデーション

- **音声入力・音声出力**: OpenAI Realtime APIによるリアルタイム音声会話
- **自然言語対話**: 「80年代で面白い映画ある？」「タイムスリップ系のアニメが見たい」といった自然な質問に対応
- **多言語対応**: 日本語・英語での会話（入力言語に応じて自動切り替え）

### 🎯 高度な検索機能

- **映画・TV番組検索**: 動画コンテンツの検索と視聴リンク提供
- **地域ベース検索**: 特定の場所を舞台にした作品の検索（例：「横浜が舞台の映画」）
- **物語コンテンツ検索**: ストーリーテリング要素に基づく作品検索（例：「魔王を倒した後の物語」）
- **WebSocket API**: リアルタイム通信による応答性の高いユーザー体験

### 🌐 Web統合機能

- **動画検索統合**: VideoCenter（映画・TV番組）、YouTube（一般動画）
- **キャッシュシステム**: SQLiteベースの検索結果キャッシュで高速応答
- **Webインターフェース**: ブラウザベースのクライアント対応

## 🛠️ 技術スタック

- **Python 3.13+**
- **OpenAI Realtime API** - 音声対話
- **LangChain** - AIエージェントフレームワーク
- **Starlette + WebSocket** - リアルタイム通信
- **Tavily API** - Web検索
- **TMDB API** - 映画・TV番組データ

## 📋 必要条件

- Python 3.13以上
- [uv](https://github.com/astral-sh/uv) パッケージマネージャー
- 以下の環境変数を設定してください：
  - `OPENAI_API_KEY`: OpenAI APIキー（Realtime API利用）
  - `TMDB_API_KEY`: TMDB APIキー（映画・TV番組データ取得）
  - `TAVILY_API_KEY`: Tavily APIキー（Web検索）

## 🚀 セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/aRaikoFunakami/media_picks.git
cd media_picks
```

### 2. 必要なパッケージのインストール

`uv` を使用して依存関係を管理します。

#### `uv` のインストール

`uv` がインストールされていない場合、以下のコマンドでインストールしてください。

```bash
pip install uv
```

#### 依存関係のインストール

以下のコマンドで必要なパッケージをインストールします。

```bash
uv sync
```

### 3. 環境変数の設定

以下の環境変数を設定してください。

#### OpenAI APIキー（必須）

```bash
export OPENAI_API_KEY="your_openai_api_key"
```

#### TMDB APIキー（必須）

```bash
export TMDB_API_KEY="your_tmdb_api_key"
```

#### Tavily APIキー（必須）

```bash
export TAVILY_API_KEY="your_tavily_api_key"
```

## 🎵 実行方法

### WebSocketサーバーの起動

CineBotサーバーを起動して、Webクライアントからの接続を受け付けます。

```bash
uv run python cine_bot_server.py
```

デフォルトで `http://localhost:8000` でサーバーが起動し、以下のエンドポイントが利用可能です：

- **Web UI**: `http://localhost:8000` - ブラウザベースのインターフェース
- **WebSocket**: `ws://localhost:8000/ws` - リアルタイム音声通信
- **ヘルスチェック**: `http://localhost:8000/health` - サーバー状態確認

### 簡易確認方法（テキストモード）

音声機能なしでテキストベースの動作確認を行う場合：

```bash
OPENAI_VOICE_TEXT_MODE=1 uv run python cine_bot_server.py
```

別のターミナルから以下のコマンドでWebSocket接続をテストできます：

```bash
wscat -c "ws://127.0.0.1:8000/ws"
```

> **注意**: `wscat`がインストールされていない場合は、`npm install -g wscat`でインストールしてください。

### 使用例

#### 音声での質問例

- 🎬 **映画検索**: "最近の面白い映画を教えて"
- 🏠 **地域ベース**: "東京を舞台にした映画を探して"
- 📚 **物語検索**: "魔王を倒した後の物語のアニメはある？"
- 📺 **TV番組**: "おすすめのドラマシリーズを教えて"
- 🎵 **音楽動画**: "猫の動画を見たい"

#### レスポンス例

```text
🎬 CineBot: 最近の人気映画をご紹介します！

1. ファンタスティック・ビーストとダンブルドアの秘密
2. ドクター・ストレンジ/マルチバース・オブ・マッドネス
3. ソニック・ザ・ムービー/ソニック VS ナックルズ

これらの作品は2024年に特に注目を集めています。どの作品に興味がありますか？
```

## 🗂️ プロジェクト構成

```text
media_picks/
├── media_picks/                    # メインパッケージ
│   ├── cine_bot.py                 # CineBotエージェント
│   ├── video_search.py             # 動画検索ツール
│   ├── location_search.py          # 地域ベース検索
│   ├── story_search.py             # 物語検索
│   ├── base_search.py              # 検索基底クラス
│   └── langchain_openai_voice/     # 音声AI拡張
├── static/                         # Webインターフェース
│   └── index.html                  # クライアント画面
├── cine_bot_server.py              # WebSocketサーバー
├── pyproject.toml                  # プロジェクト設定
├── uv.lock                         # 依存関係ロック
├── *.sqlite                        # キャッシュデータベース
└── README.md                       # このファイル
```

## 🔧 開発者向け情報

### 新しい依存関係の追加

新しいパッケージを追加する場合、以下のコマンドを使用してください。

```bash
uv add <パッケージ名>
```

### 依存関係の更新

依存関係を更新するには、以下のコマンドを使用します。

```bash
uv sync
```

### カスタムツールの追加

新しい検索機能を追加するには、`media_picks/base_search.py`を継承してカスタムツールを作成できます。

### 多言語対応の拡張

現在日本語・英語に対応していますが、他の言語も追加可能です。各ツールに`language`パラメータを渡すことで言語設定を変更できます。

## 🚨 トラブルシューティング

### 一般的な問題と解決方法

1. **APIキーエラー**: 環境変数が正しく設定されているか確認
2. **WebSocket接続エラー**: ファイアウォール設定とポート8000の開放を確認
3. **音声入力が認識されない**: ブラウザのマイク許可設定を確認

### ログの確認

サーバー起動時にログが出力されます。問題がある場合は、ログを確認してください。

```bash
# ログレベルを詳細にする場合
export LOG_LEVEL=DEBUG
uv run python cine_bot_server.py
```

## 📄 ライセンス

このプロジェクトはMITライセンスの下で提供されています。詳細は`LICENSE`ファイルをご確認ください。

## 🤝 コントリビューション

プルリクエストやイシューの報告を歓迎します。以下のガイドラインに従ってください：

1. フォークしてローカルで開発
2. 機能追加時はテストを含める
3. コードスタイルは既存のものに合わせる
4. Pull Requestを作成

---

🎬 **Media Picks - あなたの最適なエンターテインメント体験をお届けします！**
