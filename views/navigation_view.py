"""
ナビゲーション表示のView
"""

import streamlit as st
from views.page import Page


class NavigationView:
    """
    サイドバーのナビゲーション表示を管理するView。
    
    ユーザーがページを選択可能なラジオボタンをサイドバーに表示します。
    
    Attributes:
        pages (list[Page]): 利用可能なページ定義のリスト
    """
    
    def __init__(self, pages: list[Page]):
        """
        初期化処理。
        
        Args:
            pages (list[Page]): 利用可能なページのリスト
        """
        self.pages = pages
    
    def show(self) -> str:
        """
        サイドバーのナビゲーションを表示し、選択されたページIDを返す。
        
        Returns:
            str: 選択されたページのpage_id
        """
        st.sidebar.title("Navigation")
        
        page_labels = [page.label for page in self.pages]
        
        selected_label = st.sidebar.radio(
            label="Pages",
            options=page_labels,
            label_visibility="collapsed"
        )
        
        selected_page = next(
            (page for page in self.pages if page.label == selected_label),
            self.pages[0]
        )
        return selected_page.page_id
