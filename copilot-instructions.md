# Copilot 指示書 - MVC_GUI_Practice_with_Copilot

## プロジェクト概要

**プロジェクト名**: MVC_GUI_Practice_with_Copilot  
**目的**: MVCアーキテクチャパターンを採用し、PythonでGUIアプリの設計を練習する  
**主要言語**: Python  
**アーキテクチャパターン**: Model-View-Controller (MVC)

## プロジェクト構成

```
MVC_GUI_Practice_with_Copilot/
├── models/           # データ層・ビジネスロジック
├── views/            # UI・表示層
├── controllers/      # 制御層・イベント処理
├── main.py          # アプリケーション起点
├── requirements.txt # 依存ライブラリ
└── README.md        # プロジェクト説明
```

## MVCアーキテクチャ設計原則

### Model (モデル)
- **役割**: ビジネスロジックとデータ管理
- **責務**: 
  - データベースアクセス
  - ビジネスルールの実装
  - データの検証と処理
- **重要**: UIに依存しない独立した層

### View (ビュー)
- **役割**: ユーザーインターフェース
- **責務**:
  - GUI要素の定義と表示
  - ユーザー入力の受け取り
  - データの視覚化
- **重要**: ビジネスロジックを持たない

### Controller (コントローラー)
- **役割**: ModelとViewの仲介
- **責務**:
  - ユーザーイベントの処理
  - ModelからのデータをViewへ反映
  - ViewからのリクエストをModelへ転送
- **重要**: 両層の間で明確な責務分離を維持

## Python コーディング規約

### ネーミング規則
```python
# クラス名: PascalCase
class UserModel:
    pass

class LoginView:
    pass

class UserController:
    pass

# 関数・メソッド: snake_case
def get_user_data():
    pass

def validate_email(email):
    pass

# 定数: UPPER_SNAKE_CASE
MAX_USERS = 100
DATABASE_URL = "sqlite:///app.db"

# プライベート: アンダースコアで始める
def _internal_method():
    pass
```

### スタイルガイド
- **準拠基準**: PEP 8
- **インデント**: スペース4つ
- **行の長さ**: 最大79文字
- **ドキュメント**: docstring を必ず記述

### ドキュメント記述例
```python
def calculate_total_price(items, tax_rate=0.1):
    """
    商品リストの合計金額を計算する。

    Args:
        items (list): 商品辞書のリスト
        tax_rate (float): 税率（デフォルト: 0.1）

    Returns:
        float: 税金を含めた合計金額

    Raises:
        ValueError: items が空の場合
    """
    pass
```

## Copilot への効果的な指示方法

### Model関連の相談
```
「ユーザー認証ロジックをModelに実装してください」
「データベースアクセス層を抽象化するインターフェースを設計してください」
「入力値の検証ロジックを追加してください」
```

### View関連の相談
```
「tkinterでログイン画面を実装してください」
「ボタンとテキスト入力フィールドを含むフォームを作成してください」
「データを表示するテーブルウィジェットを実装してください」
```

### Controller関連の相談
```
「ボタンクリックイベントのハンドラーを実装してください」
「ログインボタンが押された時、Model経由でデータを取得し、Viewを更新するロジックを書いてください」
「エラーメッセージをViewに表示するメソッドを追加してください」
```

## 推奨技術スタック

| 項目 | 推奨 | 代替案 |
|------|------|------|
| Python バージョン | 3.9+ | 3.8+ |
| GUI フレームワーク | tkinter | PyQt6, PySimpleGUI |
| パッケージ管理 | poetry | pip, pipenv |
| テスティング | pytest | unittest |
| 型チェック | mypy | 不要 |

## コード品質基準

### 責務分離
- **単一責任の原則 (SRP)**: 各クラスは1つの理由でのみ変更される
- **依存関係の逆転 (DIP)**: 具象クラスではなく抽象クラスに依存
- **開放閉鎖の原則 (OCP)**: 拡張に開かれ、修正に閉じている

### エラーハンドリング
```python
try:
    result = model.fetch_data()
except ValueError as e:
    view.show_error("無効な入力です: " + str(e))
except ConnectionError as e:
    view.show_error("接続エラーが発生しました")
```

### テスト容易性
- Modelは UI 依存がなく、単独テストが可能
- Controllerはモック化したModel/Viewでテスト可能
- Viewはユーザーアクションのシミュレーションテストが可能

## 実装時のベストプラクティス

### 1. 層間通信の設計
```python
# Model が View に直接参照しない
# Controller を通じてのみ通信
class UserController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def on_login_clicked(self, username, password):
        try:
            user = self.model.authenticate(username, password)
            self.view.show_main_window()
        except AuthenticationError:
            self.view.show_error("認証に失敗しました")
```

### 2. イベント駆動アーキテクチャ
- GUI イベント → Controller → Model
- Model データ変更 → Controller → View 更新

### 3. 設定管理
```python
# config.py で一元管理
DATABASE_PATH = "app.db"
LOG_LEVEL = "INFO"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
```

### 4. ロギング
```python
import logging

logger = logging.getLogger(__name__)
logger.info("ユーザーがログインしました")
logger.error("データベース接続エラー: %s", str(error))
```

## Copilot チェックリスト

Copilotに以下の確認を依頼できます:

- [ ] MVCの各層が明確に分離されているか検査してください
- [ ] 循環依存がないか確認してください
- [ ] ユニットテストを作成してください
- [ ] エラーハンドリングが完全か確認してください
- [ ] PEP 8 に準拠しているか確認してください
- [ ] ドキュメントが不足していないか確認してください
- [ ] パフォーマンスの最適化提案をしてください
- [ ] セキュリティリスクがないか確認してください

## トラブルシューティング

Copilotに質問する際は、以下を含めると効果的です:

1. **何をしたいのか**: 実装したい機能の説明
2. **現在の状態**: 既存コードのスニペット
3. **エラーメッセージ**: 発生しているエラーの全文
4. **期待される結果**: 目指す動作

### 相談例
```
「ユーザーがテキストフィールドに入力して送信ボタンをクリックしたとき、
 その入力値をModelで検証し、有効な場合はデータベースに保存、
 無効な場合は画面にエラーメッセージを表示したいです。
 このフローをMVC構造で実装してください。」
```

## 参考資料

- **MVC設計パターン**: 層間の責務分離を常に意識
- **PEP 8**: https://pep8-ja.readthedocs.io/ja/latest/
- **Python型ヒント**: type hints を活用してコード品質向上

---

**作成日**: 2026-04-04  
**対象プロジェクト**: MVC_GUI_Practice_with_Copilot
