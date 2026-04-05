"""
MVC_GUI_Practice_with_Copilot - アプリケーション起点

Streamlitを使用したダッシュボードアプリケーション。
MVCアーキテクチャに基づき、Views層と協調してページ管理を行う。

このモジュールはアプリケーションの起点のみを担当し、
UI表示処理はViews層に委譲します。
"""

import streamlit as st
from views.views import configure_page, Page, NavigationView, ContentView, QuizView


def main():
    """
    メインアプリケーション処理。
    
    ページ定義、Views層のインスタンス化、
    ページ表示フローを管理します。
    """
    # ページ設定
    configure_page()
    
    # ページ定義を値オブジェクトで一元管理
    pages = [
        Page(
            label="出題",
            page_id="quiz",
            title="足し算問題",
            content="問題が表示されます"
        ),
        Page(
            label="結果",
            page_id="result",
            title="判定結果",
            content="判定結果が表示されます"
        ),
    ]
    
    # Views層のインスタンス化
    navigation_view = NavigationView(pages)
    content_view = ContentView(pages)
    quiz_view = QuizView()
    
    # ナビゲーション表示と選択ページ取得
    selected_page_id = navigation_view.show()
    
    # ページIDに応じた表示
    if selected_page_id == "quiz":
        st.title("足し算問題")
        quiz_view.show()
    else:
        # その他のページ
        content_view.show(selected_page_id)


if __name__ == "__main__":
    main()
