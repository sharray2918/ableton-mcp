# AbletonMCP Remote Script - Core Module

## 概要

AbletonMCP Remote Scriptのcoreモジュールは、以下の3つのファイルにリファクタリングされました：

## ファイル構成

### `main.py` - メインコントローラー
- `AbletonMCP`クラス: Ableton Liveのコントロールサーフェースのメインエントリーポイント
- ハンドラーの初期化と管理
- コマンド処理のルーティング
- メインスレッドでの操作実行

**主要クラス:**
- `AbletonMCP`: Ableton Liveとの統合を管理するメインクラス

**主要メソッド:**
- `__init__()`: コントロールサーフェースの初期化
- `disconnect()`: クリーンアップ処理
- `_process_command()`: クライアントからのコマンドを処理
- `_handle_main_thread_command()`: メインスレッドでの実行が必要なコマンドを処理

### `server.py` - ソケットサーバー
- TCP/IPソケットサーバーの管理
- クライアント接続の受け入れ
- サーバーのライフサイクル管理
- マルチスレッド対応

**主要クラス:**
- `SocketServer`: TCP/IPサーバーの実装

**主要メソッド:**
- `start()`: サーバーの開始
- `stop()`: サーバーの停止
- `set_client_handler()`: クライアント処理コールバックの設定
- `_server_thread()`: サーバースレッドの実装

### `client.py` - クライアント処理
- 個別クライアント接続の処理
- メッセージの送受信
- JSON形式でのコマンド/レスポンス処理
- Python 2/3互換性

**主要クラス:**
- `ClientHandler`: クライアント接続とメッセージ処理

**主要メソッド:**
- `handle_client()`: クライアント通信の処理
- `set_running()`: 実行状態の制御
- `_send_response()`: レスポンスの送信

## アーキテクチャの利点

### 1. 責任の分離
- **main.py**: Ableton Liveとの統合とビジネスロジック
- **server.py**: ネットワーク通信のインフラストラクチャ
- **client.py**: クライアント固有の処理

### 2. テスト可能性の向上
- 各コンポーネントを独立してテスト可能
- モック化が容易
- 単体テストの作成が簡単

### 3. 保守性の向上
- コードの可読性向上
- 機能別の明確な分離
- デバッグの簡素化

### 4. 拡張性
- 新しいサーバー実装の追加が容易
- クライアント処理の独立した改善
- 機能追加時の影響範囲の最小化

## 使用例

```python
# メインコントローラーの初期化
mcp = AbletonMCP(c_instance)

# サーバーとクライアントハンドラーは自動的に初期化される
# ポート9877でクライアント接続を待機
```

## Python 2/3 互換性

すべてのモジュールはPython 2とPython 3の両方をサポートするように設計されています：

- 文字列エンコーディングの適切な処理
- `queue`/`Queue`モジュールの互換性
- `socket`操作の互換性

## エラー処理

各モジュールには堅牢なエラー処理が実装されています：

- 接続エラーの適切な処理
- タイムアウト処理
- リソースのクリーンアップ
- ログ出力による診断情報の提供

## 設定

デフォルト設定：
- ホスト: `localhost`
- ポート: `9877`
- 接続タイムアウト: 1秒
- コマンド実行タイムアウト: 10秒

これらの設定は必要に応じて各クラスの初期化時に変更可能です。
