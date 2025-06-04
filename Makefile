.PHONY: help lint format check test install-dev clean

help: ## このヘルプメッセージを表示
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-dev: ## 開発依存関係をインストール
	uv sync --group dev

install-pre-commit: ## pre-commitフックをインストール
	uv run pre-commit install

lint: ## Ruffでコードをlint
	uv run ruff check .

lint-fix: ## Ruffでコードをlintし、修正可能な問題を自動修正（未使用変数の削除含む）
	uv run ruff check --fix --unsafe-fixes .

format: ## Ruffでコードをフォーマット
	uv run ruff format .

format-check: ## フォーマットが必要かどうかをチェック（CI用）
	uv run ruff format --check .

type-check: ## MyPyで型チェック
	uv run mypy MCP_Server/

check: lint format-check type-check ## 全てのチェックを実行

test: ## テストを実行
	uv run pytest

clean: ## キャッシュファイルを削除
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

setup: install-dev install-pre-commit ## 開発環境をセットアップ
	@echo "開発環境のセットアップが完了しました"
	@echo "利用可能なコマンド:"
	@make help
