"""
Views層 - UI・表示処理

ページ定義、ナビゲーション、クイズ出題、結果表示を管理します。

設計原則：
- 値オブジェクト（Page）でページ定義を一元化
- 単一責任原則：各Viewクラスは1つの表示責務のみ
- オープン・クローズド原則：新ページ追加時に既存クラスを修正しない
"""

from views.page import Page
from views.navigation_view import NavigationView
from views.quiz_view import QuizView
from views.result_view import ResultView
from views.configure_page import configure_page

__all__ = [
    "Page",
    "NavigationView",
    "QuizView",
    "ResultView",
    "configure_page",
]

