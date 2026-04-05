"""
Views層 - UI・表示処理

ページ定義、サイドバー、メインコンテンツの表示を
OOP設計に基づいて管理します。

設計原則：
- 値オブジェクト（Page）でページ定義を一元化
- 単一責任原則：各Viewクラスは1つの表示責務のみ
- オープン・クローズド原則：新ページ追加時に既存クラスを修正しない
"""

import streamlit as st
import random


class Page:
    """
    ページ定義を表す値オブジェクト。
    
    ページに関連するすべての情報を不変にカプセル化します。
    
    Attributes:
        label (str): ナビゲーションメニューに表示されるテキスト
        page_id (str): ページを識別する内部ID
        title (str): ページ本体に表示されるタイトル
        content (str): ページに表示されるコンテンツ
    """
    
    def __init__(self, label: str, page_id: str, title: str, content: str):
        self.label = label
        self.page_id = page_id
        self.title = title
        self.content = content
    
    def __eq__(self, other):
        """ページ定義の同一性を判定"""
        if not isinstance(other, Page):
            return False
        return self.page_id == other.page_id
    
    def __hash__(self):
        """ページをセットのキーとして使用可能にする"""
        return hash(self.page_id)


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
        
        # ページのラベルリスト
        page_labels = [page.label for page in self.pages]
        
        # ユーザーの選択を取得
        selected_label = st.sidebar.radio(
            label="Pages",
            options=page_labels,
            label_visibility="collapsed"
        )
        
        # 選択されたラベルに対応するpage_idを返す
        selected_page = next(
            (page for page in self.pages if page.label == selected_label),
            self.pages[0]  # フォールバック
        )
        return selected_page.page_id


class ContentView:
    """
    メインコンテンツ表示を管理するView。
    
    指定されたページIDに対応するコンテンツを表示します。
    
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
    
    def show(self, page_id: str):
        """
        指定されたページIDに対応するコンテンツを表示する。
        
        Args:
            page_id (str): 表示するページのID
        """
        # page_idに対応するページを検索
        page = next(
            (page for page in self.pages if page.page_id == page_id),
            None
        )
        
        if page:
            st.title(page.title)
            st.write(page.content)
        else:
            st.error(f"Page '{page_id}' not found.")


def configure_page():
    """
    ページの初期設定を行う。
    
    Streamlitの基本的なページ設定（タイトル、レイアウト、サイドバー状態）を実施します。
    """
    st.set_page_config(
        page_title="Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )


class QuizView:
    """
    足し算問題の出題と入力を管理するView。
    
    1桁の正の整数の足し算をランダムに生成し、
    ユーザーが答えを入力できるフォームを提供します。
    
    Attributes:
        quiz_session_key (str): Streamlit session_state のキー
    """
    
    QUIZ_SESSION_KEY = "quiz_data"
    
    def __init__(self):
        """初期化処理。"""
        self._initialize_session()
    
    def _initialize_session(self):
        """
        Streamlit session_state を初期化する。
        
        初回アクセス時に新しい問題を生成します。
        """
        if self.QUIZ_SESSION_KEY not in st.session_state:
            st.session_state[self.QUIZ_SESSION_KEY] = self._generate_quiz()
    
    def _generate_quiz(self):
        """
        足し算問題を生成する。
        
        Returns:
            dict: {'num1': int, 'num2': int, 'answer': int} を含む辞書
        """
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        return {
            'num1': num1,
            'num2': num2,
            'answer': num1 + num2
        }
    
    def show(self):
        """
        問題表示フォームと提出ボタンを表示する。
        """
        quiz_data = st.session_state[self.QUIZ_SESSION_KEY]
        
        # 問題表示
        st.write(f"### {quiz_data['num1']} + {quiz_data['num2']} = ?")
        
        # 入力フォーム
        user_answer = st.number_input(
            label="答えを入力してください",
            min_value=0,
            max_value=18,
            step=1,
            key="user_answer"
        )
        
        # 提出ボタン
        if st.button("結果提出"):
            st.session_state['submitted_answer'] = user_answer
            st.rerun()


