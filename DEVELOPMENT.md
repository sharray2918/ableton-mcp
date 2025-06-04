# 開発ガイド

このプロジェクトでは、Python3のlintとフォーマットのツールが設定されています。

## 必要なツール

- **Ruff**: 高速なlinter/formatter（lintとフォーマットを両方対応）
- **MyPy**: 型チェッカー
- **Pre-commit**: コミット前フック

## セットアップ

```bash
# 開発環境をセットアップ（依存関係とpre-commitをインストール）
make setup
```

## 利用可能なコマンド

### Lint関連
```bash
# コードをlint
make lint

# lintエラーを自動修正
make lint-fix
```

### フォーマット関連
```bash
# コードをフォーマット
make format

# フォーマットが必要かチェック（CI用）
make format-check
```

### 型チェック
```bash
# MyPyで型チェック
make type-check
```

### 総合チェック
```bash
# 全てのチェックを実行（lint + format-check + type-check）
make check
```

### その他
```bash
# テストを実行
make test

# キャッシュファイルを削除
make clean

# 利用可能なコマンドを表示
make help
```

## VS Code設定

`.vscode/settings.json`で以下の設定が有効になっています：

- ファイル保存時の自動フォーマット
- インポートの自動整理
- Ruffによるlint
- MyPyによる型チェック

## Pre-commit フック

コミット前に自動的に以下が実行されます：

- Ruffによるlintと自動修正
- Ruffによるフォーマット
- 基本的なファイルチェック（末尾の空白、YAML/TOML/JSONの文法チェックなど）

## 推奨ワークフロー

1. コードを編集
2. `make format` でフォーマット
3. `make lint-fix` でlintエラーを修正
4. `make check` で全体チェック
5. コミット（pre-commitフックが自動実行）

## 設定ファイル

- `pyproject.toml`: Ruff、MyPyの設定
- `.pre-commit-config.yaml`: Pre-commitフックの設定
- `.vscode/settings.json`: VS Codeの設定
- `Makefile`: 開発用コマンド
