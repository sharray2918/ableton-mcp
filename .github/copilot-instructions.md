# Python 開発に特化した AI アシスタントのルール

## 基本方針
- **プロジェクト構造**: ソースコード、テスト、ドキュメント、設定ファイルを分離したディレクトリ構造を採用。
- **モジュール設計**: モデル、サービス、コントローラー、ユーティリティを個別のファイルに分割。
- **設定管理**: 環境変数を使用して設定を管理。
- **エラー処理とログ**: コンテキストを含む堅牢なエラー処理とログ機能を実装。
- **テスト**: pytest を使用した包括的なテスト。
- **ドキュメント**: Docstring と README ファイルを用いた詳細なドキュメント作成。
- **依存関係管理**: [astral-sh/uv](https://github.com/astral-sh/uv) と仮想環境を利用。
- **コードスタイル**: Ruff を使用してコードスタイルを統一。
- **CI/CD**: GitHub Actions または GitLab CI を活用した CI/CD の実装。

## AI フレンドリーなコーディングプラクティス
- これらの原則に基づき、明確で AI 支援に最適化されたコードスニペットと説明を提供。

## 詳細ルール
1. **型アノテーション**:
   - Python ファイルでは、すべての関数やクラスに型アノテーションを追加すること。
   - 必要に応じて戻り値の型も含める。
   - すべての関数やクラスに説明的な Docstring を追加すること。
   - Docstring は PEP257 規約に従うこと。
   - 既存の Docstring がある場合は必要に応じて更新する。

2. **コメント保持**:
   - ファイル内に既存のコメントがある場合は削除せず保持する。

3. **テスト**:
   - テストには pytest または pytest プラグインのみを使用し、unittest モジュールは使用しない。
   - テストには型アノテーションを追加すること。
   - テストは `./tests` ディレクトリ内に配置する。
   - 必要なファイルやフォルダを作成すること。
   - `./tests` または `./src/goob_ai` 内にファイルを作成する場合、`__init__.py` ファイルが存在しない場合は作成する。

4. **テストの詳細**:
   - テストは完全に型アノテーションを含むこと。
   - Docstring を含むこと。
   - `TYPE_CHECKING` を使用する場合、以下をインポートすること:
     ```python
     from _pytest.capture import CaptureFixture
     from _pytest.fixtures import FixtureRequest
     from _pytest.logging import LogCaptureFixture
     from _pytest.monkeypatch import MonkeyPatch
     from pytest_mock.plugin import MockerFixture
     ```
