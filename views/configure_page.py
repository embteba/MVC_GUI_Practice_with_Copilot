"""
ページ設定
"""

import streamlit as st


def configure_page():
    """
    ページの初期設定を行う。
    
    Streamlitの基本的なページ設定（タイトル、レイアウト、サイドバー状態）を実施します。
    """
    st.set_page_config(
        page_title="Quiz App",
        layout="wide",
        initial_sidebar_state="expanded"
    )
