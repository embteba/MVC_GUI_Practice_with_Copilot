# MVC_GUI_Practice_with_Copilot - アーキテクチャドキュメント

## 概要

1桁の正の整数の足し算クイズアプリケーション。  
MVCアーキテクチャパターンに基づき、Streamlit で構築されています。

---

## プロジェクト構成

```
MVC_GUI_Practice_with_Copilot/
├── main.py                    # アプリケーション起点
├── config.py                  # 共通定数管理
├── models/
│   ├── __init__.py
│   └── quiz_model.py          # QuizModel（判定ロジック）
├── views/
│   ├── __init__.py             # Views層パッケージ（公開API一元管理）
│   ├── configure_page.py       # ページ設定
│   ├── page.py                 # Page（値オブジェクト）
│   ├── navigation_view.py      # NavigationView（サイドバー）
│   ├── quiz_view.py            # QuizView（出題画面）
│   ├── result_view.py          # ResultView（結果画面）
│   └── quiz_helper.py          # 問題生成の共通処理
├── controllers/
│   ├── __init__.py
│   └── quiz_controller.py      # QuizController（フロー制御）
└── requirements.txt
```

---

## クラス関係図

```mermaid
classDiagram
    direction TB

    class main {
        +main()
    }

    class config {
        QUIZ_DATA_KEY
        SUBMITTED_ANSWER_KEY
        CURRENT_PAGE_KEY
        PAGE_ID_QUIZ
        PAGE_ID_RESULT
        PAGE_LABEL_QUIZ
        PAGE_LABEL_RESULT
        PAGE_TITLE_QUIZ
        PAGE_TITLE_RESULT
        QUIZ_MIN_VALUE
        QUIZ_MAX_VALUE
        QUIZ_INPUT_MIN
        QUIZ_INPUT_MAX
    }

    class QuizController {
        -pages: list~Page~
        -navigation_view: NavigationView
        -quiz_view: QuizView
        -result_view: ResultView
        +run()
        -_create_pages() Page[]
        -_resolve_page_id(str) str
        -_display_page(str)
    }

    class Page {
        +label: str
        +page_id: str
        +title: str
    }

    class NavigationView {
        -pages: list~Page~
        +show() str
    }

    class QuizView {
        +QUIZ_SESSION_KEY: str
        -_initialize_session()
        +show()
    }

    class ResultView {
        +show()
    }

    class QuizModel {
        +judge_answer(int, int)$ dict
    }

    class quiz_helper {
        +generate_quiz() dict
    }

    class configure_page {
        +configure_page()
    }

    main --> configure_page : ページ設定
    main --> QuizController : 制御を委譲

    QuizController --> NavigationView : サイドバー表示
    QuizController --> QuizView : 出題ページ表示
    QuizController --> ResultView : 結果ページ表示
    QuizController --> Page : ページ定義を生成

    NavigationView --> Page : ページ一覧を参照

    QuizView --> quiz_helper : 問題生成
    ResultView --> quiz_helper : 新問題生成
    ResultView --> QuizModel : 回答判定

    QuizView ..> config : 定数参照
    ResultView ..> config : 定数参照
    QuizController ..> config : 定数参照
    quiz_helper ..> config : 定数参照
```

### 関係の種類

| 記号 | 意味 |
|------|------|
| 実線矢印（→） | 直接的な依存（インスタンス保持・メソッド呼び出し） |
| 点線矢印（..>） | 定数参照のみの間接的な依存 |

---

## シーケンス図

```mermaid
sequenceDiagram
    autonumber
    actor User as ユーザー

    participant main as main.py
    participant cfg as configure_page
    participant ctrl as QuizController
    participant nav as NavigationView
    participant qv as QuizView
    participant rv as ResultView
    participant qh as quiz_helper
    participant model as QuizModel
    participant ss as session_state

    Note over main,model: === アプリ起動 ===
    main->>cfg: configure_page()
    main->>ctrl: QuizController()
    ctrl->>ctrl: _create_pages()
    ctrl->>nav: NavigationView(pages)
    ctrl->>qv: QuizView()
    qv->>ss: quiz_data 存在確認
    alt 初回アクセス
        qv->>qh: generate_quiz()
        qh-->>qv: {num1, num2, answer}
        qv->>ss: quiz_data を保存
    end
    ctrl->>rv: ResultView()
    main->>ctrl: run()

    Note over main,model: === ページ表示フロー ===
    ctrl->>nav: show()
    nav-->>ctrl: selected_page_id
    ctrl->>ctrl: _resolve_page_id()
    ctrl->>ss: current_page 確認
    alt current_page あり（ボタン遷移）
        ss-->>ctrl: page_id
        ctrl->>ss: current_page 削除
    end

    alt 出題ページ選択
        ctrl->>qv: show()
        qv->>ss: quiz_data 取得
        qv-->>User: 問題表示 + 入力フォーム
        User->>qv: 回答入力 + 結果提出ボタン
        qv->>ss: submitted_answer 保存
        qv->>ss: current_page = result
        qv->>qv: st.rerun()
    end

    alt 結果ページ選択
        ctrl->>rv: show()
        rv->>ss: quiz_data, submitted_answer 取得
        rv->>model: judge_answer(correct, user)
        model-->>rv: {is_correct, message, ...}
        rv-->>User: 判定結果表示
        User->>rv: 新しい問題に挑戦ボタン
        rv->>qh: generate_quiz()
        qh-->>rv: {num1, num2, answer}
        rv->>ss: quiz_data 更新
        rv->>ss: submitted_answer 削除
        rv->>ss: current_page = quiz
        rv->>rv: st.rerun()
    end
```

### フェーズ説明

| フェーズ | ステップ | 内容 |
|----------|----------|------|
| アプリ起動 | 1〜11 | main → Controller → 各View初期化 |
| ページ表示フロー | 12〜16 | ナビゲーション表示 → ページ遷移解決 |
| ユーザー操作 | 17〜30 | 出題 ↔ 結果 の循環フロー |

---

## 各層の責務

### Model層（models/）

| クラス | 責務 |
|--------|------|
| `QuizModel` | 回答の正誤判定（静的メソッド） |

- UIに依存しない独立した層
- 純粋なビジネスロジックのみ

### View層（views/）

| クラス/モジュール | 責務 |
|-------------------|------|
| `Page` | ページ定義の値オブジェクト |
| `NavigationView` | サイドバーのナビゲーション表示 |
| `QuizView` | 足し算問題の出題と入力フォーム |
| `ResultView` | 判定結果の表示と再チャレンジ |
| `quiz_helper` | 問題生成の共通処理 |
| `configure_page` | Streamlitページ設定 |

- ビジネスロジックを持たない
- UI表示のみを担当

### Controller層（controllers/）

| クラス | 責務 |
|--------|------|
| `QuizController` | ページ定義管理、Views協調、ページ遷移制御 |

- ModelとViewの仲介
- アプリケーション全体のフロー統括

### 共通モジュール

| モジュール | 責務 |
|------------|------|
| `config.py` | session_stateキー、ページID/ラベル/タイトル、クイズ設定の定数管理 |

---

## 設計原則

| 原則 | 適用箇所 |
|------|----------|
| 単一責任原則（SRP） | 各クラスが1つの責務のみを持つ |
| YAGNI原則 | 現在必要な機能のみ実装 |
| オープン・クローズド原則（OCP） | 新ページ追加時に既存クラスを修正しない |
| DRY原則 | quiz_helper で問題生成を共通化 |
| 高凝集・疎結合 | MVCの各層が独立し、config で定数を一元管理 |
