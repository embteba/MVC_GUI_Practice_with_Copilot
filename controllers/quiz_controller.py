"""
Controllers層 - クイズアプリケーションの制御

ModelとViewを仲介し、アプリケーション全体のフロー制御を行います。
"""

import streamlit as st
from views import Page, NavigationView, QuizView, ResultView
from config import (
    PAGE_ID_QUIZ, PAGE_ID_RESULT,
    PAGE_LABEL_QUIZ, PAGE_LABEL_RESULT,
    PAGE_TITLE_QUIZ, PAGE_TITLE_RESULT,
    CURRENT_PAGE_KEY
)


class QuizController:
    """
    クイズアプリケーションのメイン制御を担当するコントローラー。
    
    ページ定義、Views層の操作、ページ遷移を統括します。
    
    Attributes:
        pages (list[Page]): ページ定義のリスト
        navigation_view (NavigationView): ナビゲーション表示View
        quiz_view (QuizView): 出題View
        result_view (ResultView): 結果表示View
    """
    
    def __init__(self):
        """初期化処理。"""
        self.pages = self._create_pages()
        self.navigation_view = NavigationView(self.pages)
        self.quiz_view = QuizView()
        self.result_view = ResultView()
    
    @staticmethod
    def _create_pages():
        """
        ページ定義を作成する。
        
        Returns:
            list[Page]: ページ定義のリスト
        """
        return [
            Page(
                label=PAGE_LABEL_QUIZ,
                page_id=PAGE_ID_QUIZ,
                title=PAGE_TITLE_QUIZ
            ),
            Page(
                label=PAGE_LABEL_RESULT,
                page_id=PAGE_ID_RESULT,
                title=PAGE_TITLE_RESULT
            ),
        ]
    
    def run(self):
        """
        アプリケーション全体のフロー制御。
        
        ナビゲーション表示、ページ遷移、View表示を統括します。
        """
        # ナビゲーション表示（常にサイドバーを表示）
        selected_page_id = self.navigation_view.show()
        
        # セッション状態でページ遷移が指定されている場合、それを優先
        selected_page_id = self._resolve_page_id(selected_page_id)
        
        # ページを表示
        self._display_page(selected_page_id)
    
    @staticmethod
    def _resolve_page_id(navigation_page_id: str) -> str:
        """
        セッション状態からページIDを解決する。
        
        ボタン押下時の自動遷移を優先し、その後削除します。
        
        Args:
            navigation_page_id (str): ナビゲーションから選択されたページID
        
        Returns:
            str: 表示するページID
        """
        if CURRENT_PAGE_KEY in st.session_state:
            page_id = st.session_state[CURRENT_PAGE_KEY]
            del st.session_state[CURRENT_PAGE_KEY]
            return page_id
        return navigation_page_id
    
    def _display_page(self, page_id: str):
        """
        指定されたページIDに対応するページを表示する。
        
        Args:
            page_id (str): ページID
        """
        if page_id == PAGE_ID_QUIZ:
            st.title(PAGE_TITLE_QUIZ)
            self.quiz_view.show()
        elif page_id == PAGE_ID_RESULT:
            st.title(PAGE_TITLE_RESULT)
            self.result_view.show()

