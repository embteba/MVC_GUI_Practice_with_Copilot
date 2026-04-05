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

## 設計原則

このプロジェクトは以下の設計原則に厳密に従います。

### 1. 単一責任原則 (Single Responsibility Principle - SRP)

**定義**: 各クラス・関数は、変更の理由が1つだけであるべき。1つの責務のみを持つ。

**実装例**:
```python
# ❌ 悪い例：複数の責務を持つ
class UserManager:
    def create_user(self, name, email):
        # ユーザー作成と検証の両方を行う
        if not self._validate_email(email):
            raise ValueError("Invalid email")
        self.db.insert_user(name, email)
    
    def _validate_email(self, email):
        # メール検証
        return "@" in email
    
    def save_to_file(self):
        # ファイル保存
        with open("users.txt", "w") as f:
            f.write(str(self.users))

# ✅ 良い例：責務を分離
class EmailValidator:
    """メール検証のみを責務とする"""
    def validate(self, email):
        return "@" in email and "." in email.split("@")[1]

class UserModel:
    """ユーザーのビジネスロジックのみを責務とする"""
    def __init__(self, validator):
        self.validator = validator
    
    def create_user(self, name, email):
        if not self.validator.validate(email):
            raise ValueError("Invalid email")
        return {"name": name, "email": email}

class UserRepository:
    """データベースアクセスのみを責務とする"""
    def save(self, user):
        self.db.insert_user(user)
```

**チェックポイント**:
- クラスの名前に「Manager」「Handler」「Processor」と複数の動詞が含まれないか
- クラスの変更理由が複数ないか
- 各メソッドが1つの目的を果たしているか

---

### 2. YAGNI原則 (You Aren't Gonna Need It)

**定義**: 必要になるまで機能を実装しない。将来の可能性のために不要なコードを書かない。

**実装例**:
```python
# ❌ 悪い例：未来に「必要かもしれない」機能を実装
class DataProcessor:
    def process(self, data):
        result = self._advanced_processing(data)
        result = self._future_optimization_1(result)
        result = self._future_optimization_2(result)
        return result
    
    def _advanced_processing(self, data):
        # 現在は使われない高度な処理
        pass
    
    def _future_optimization_1(self, data):
        # 将来必要になるかもしれない最適化（今は未使用）
        pass
    
    def _future_optimization_2(self, data):
        # やはり将来必要になるかもしれない（今は未使用）
        pass

# ✅ 良い例：現在必要な機能のみ実装
class DataProcessor:
    def process(self, data):
        return self._convert_to_dict(data)
    
    def _convert_to_dict(self, data):
        # 今すぐ必要な機能のみ
        return dict(data)
```

**チェックポイント**:
- 未使用のメソッド・パラメータはないか
- 「念のため」のためだけに複雑性を追加していないか
- 「もしかして後で使うかも」というコードがないか
- テストされていない機能がないか
- **先読み生成（先制的なファイル/コード生成）していないか**

---

### 3. オープン・クローズド原則 (Open/Closed Principle - OCP)

**定義**: ソフトウェアは拡張に対して開かれ、変更に対して閉じられるべき。
新機能を追加するときに既存コードを変更しない設計。

**実装例**:
```python
# ❌ 悪い例：新機能追加のたびに既存クラスを変更
class ReportGenerator:
    def generate(self, report_type):
        if report_type == "pdf":
            # PDF生成ロジック
            return self._generate_pdf()
        elif report_type == "csv":
            # CSV生成ロジック
            return self._generate_csv()
        elif report_type == "json":
            # JSON生成ロジック（新機能追加で修正が必要）
            return self._generate_json()
        # Excel対応を追加するときもここを修正...

# ✅ 良い例：多態性を使って拡張に対して開かれた設計
from abc import ABC, abstractmethod

class Exporter(ABC):
    """抽象基底クラス"""
    @abstractmethod
    def export(self, data):
        pass

class PDFExporter(Exporter):
    def export(self, data):
        return f"PDF: {data}"

class CSVExporter(Exporter):
    def export(self, data):
        return f"CSV: {data}"

class JSONExporter(Exporter):
    def export(self, data):
        return f"JSON: {data}"

class ReportGenerator:
    """既存コードは変更せず、新しいExporter を追加するだけで拡張可能"""
    def __init__(self, exporter: Exporter):
        self.exporter = exporter
    
    def generate(self, data):
        return self.exporter.export(data)

# 新しい形式を追加する場合：既存コードを一切変更しない
class ExcelExporter(Exporter):
    def export(self, data):
        return f"Excel: {data}"
```

**チェックポイント**:
- 新機能追加時に既存のクラス・関数を修正していないか
- 多態性（インターフェース、抽象クラス）を活用しているか
- 「修正に対して閉じている」が「拡張に対して開いている」か
- Strategy パターン、Template Method パターン、Factory パターンの活用を検討したか

---

## OOP設計思想

### 1. 値オブジェクト (Value Object)

**定義**: ビジネス意味のあるデータや制約をカプセル化したオブジェクト。
不変で、その値によってのみ同一性が決まる。

**目的**:
- **誤実装の防止**: ドメインルールをコード上で強制
- **コードの可読性向上**: 単なる文字列や数値ではなく、意味を持つ型として表現

**実装例**:
```python
# ❌ 悪い例：プリミティブ型を直接使用
class User:
    def __init__(self, name, email, age):
        self.name = name  # 文字列のまま、制約がない
        self.email = email  # メール形式の検証がない
        self.age = age  # 負の値や不正な値が入る可能性

    def display(self):
        print(f"{self.name} ({self.age}): {self.email}")

# 使用例：誤実装が防げない
user = User("太郎", "invalid-email", -5)  # 不正なデータが許容される

# ✅ 良い例：値オブジェクトでビジネスルールを実装
class Email:
    """メールアドレスの値オブジェクト"""
    def __init__(self, value: str):
        if "@" not in value or "." not in value.split("@")[1]:
            raise ValueError(f"Invalid email: {value}")
        self._value = value
    
    def __str__(self):
        return self._value
    
    def __eq__(self, other):
        return isinstance(other, Email) and self._value == other._value

class Age:
    """年齢の値オブジェクト"""
    def __init__(self, value: int):
        if not isinstance(value, int) or value < 0 or value > 150:
            raise ValueError(f"Invalid age: {value}")
        self._value = value
    
    def __int__(self):
        return self._value
    
    def __eq__(self, other):
        return isinstance(other, Age) and self._value == other._value

class Name:
    """名前の値オブジェクト"""
    def __init__(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("Name cannot be empty")
        self._value = value.strip()
    
    def __str__(self):
        return self._value
    
    def __eq__(self, other):
        return isinstance(other, Name) and self._value == other._value

class User:
    def __init__(self, name: Name, email: Email, age: Age):
        self.name = name
        self.email = email
        self.age = age

    def display(self):
        print(f"{self.name} ({int(self.age)}): {self.email}")

# 使用例：不正なデータは即座に拒否される
try:
    user = User(
        Name("太郎"),
        Email("invalid-email"),  # ValueError: Invalid email
        Age(25)
    )
except ValueError as e:
    print(f"Error: {e}")
```

**チェックポイント**:
- データにビジネスルールが組み込まれているか
- 不正な状態が生成されないか
- 値の同一性テストが適切か
- イミュータビリティ（不変性）が保証されているか

---

### 2. 高凝集・疎結合

**定義**:
- **高凝集 (High Cohesion)**: 関連する処理・データを同じモジュール内に集める。各クラスの責務が明確で統一されている。
- **疎結合 (Low Coupling)**: モジュール間の依存を最小化する。変更の影響を局所化する。

**実装例**:
```python
# ❌ 悪い例：低凝集・高結合
class UserService:
    def __init__(self):
        self.db_connection = None
        self.email_client = None
        self.logger = None
    
    def create_user(self, name, email, password):
        # データベース操作
        self.db_connection.execute(f"INSERT INTO users VALUES...")
        # メール送信
        self.email_client.send(f"Welcome {name}")
        # ログ記録
        self.logger.info(f"User created: {email}")
        # UI更新
        self.update_ui()
    
    def update_ui(self):
        # UI更新ロジック
        pass

# ✅ 良い例：高凝集・疎結合
# 各クラスが1つの責務を持つ
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class UserRepository:
    """データベースアクセスのみ"""
    def save(self, user: User):
        # INSERT処理
        pass

class EmailNotifier:
    """メール通知のみ"""
    def send_welcome_email(self, email: str):
        # メール送信
        pass

class UserLogger:
    """ログ記録のみ"""
    def log_user_created(self, email: str):
        # ログ記録
        pass

class UserCreationService:
    """ユーザー作成の個調整"""
    def __init__(self, repository: UserRepository, notifier: EmailNotifier, logger: UserLogger):
        # 依存性をコンストラクタインジェクション
        self.repository = repository
        self.notifier = notifier
        self.logger = logger
    
    def create_user(self, name: str, email: str) -> User:
        user = User(name, email)
        self.repository.save(user)
        self.notifier.send_welcome_email(email)
        self.logger.log_user_created(email)
        return user

# 利用例：各コンポーネントが独立している
repository = UserRepository()
notifier = EmailNotifier()
logger = UserLogger()
service = UserCreationService(repository, notifier, logger)
user = service.create_user("太郎", "taro@example.com")
```

**メリット**:
- **変更の影響が限定**: メール送信ロジックの変更が、ユーザー作成には影響しない
- **テストが容易**: 各クラスを独立してテストできる（Mock を使用）
- **再利用性が向上**: `EmailNotifier` は他のサービスでも使える
- **拡張が簡単**: 新しい機能（例：SMS通知）を追加する際、既存コードを変更しない

**チェックポイント**:
- クラスの関連度が高いか（高凝集）
- クラス間の依存が最小か（疎結合）
- 依存性の注入（DI）が使われているか
- 各クラスが変更の理由を1つだけ持つか
- テストが容易か

---

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

---

## コード生成ガイドライン

### 大規模変更の事前承認

**重要**: 生成コードが **100行を超える場合**、以下のプロセスを必須とします。

1. **変更計画の提示**
   - 変更の目的と概要を明記
   - 影響するファイルと範囲を列記
   - 設計原則との適合性を説明

2. **ユーザー承認待ち**
   - 計画をユーザーに提示
   - ユーザーからの明示的な実行許可を待つ
   - 修正・調整の指示があれば反映

3. **実行と確認**
   - ユーザー承認後にコード生成
   - 実装後、設計原則の順守を確認

**目的**: 大規模変更による設計状況の低下を防ぎ、プロジェクト全体の一貫性を保つ
