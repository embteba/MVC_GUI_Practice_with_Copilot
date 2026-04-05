"""
足し算問題の出題を行うView
"""

import streamlit as st
from views.quiz_helper import generate_quiz
from config import QUIZ_DATA_KEY, SUBMITTED_ANSWER_KEY, CURRENT_PAGE_KEY, PAGE_ID_RESULT, QUIZ_INPUT_MIN, QUIZ_INPUT_MAX


class QuizView:
    """
    足し算問題の出題と入力を管理するView。
    
    1桁の正の整数の足し算をランダムに生成し、
    ユーザーが答えを入力できるフォームを提供します。
    """
    
    def __init__(self):
        """初期化処理。"""
        self._initialize_session()
    
    def _initialize_session(self):
        """
        Streamlit session_state を初期化する。
        
        初回アクセス時に新しい問題を生成します。
        """
        if QUIZ_DATA_KEY not in st.session_state:
            st.session_state[QUIZ_DATA_KEY] = generate_quiz()
    
    def show(self):
        """
        問題表示フォームと提出ボタンを表示する。
        """
        quiz_data = st.session_state[QUIZ_DATA_KEY]
        
        st.write(f"### {quiz_data['num1']} + {quiz_data['num2']} = ?")
        
        user_answer = st.number_input(
            label="答えを入力してください",
            min_value=QUIZ_INPUT_MIN,
            max_value=QUIZ_INPUT_MAX,
            step=1,
            key="user_answer"
        )
        
        if st.button("結果提出"):
            st.session_state[SUBMITTED_ANSWER_KEY] = user_answer
            st.session_state[CURRENT_PAGE_KEY] = PAGE_ID_RESULT
            st.rerun()
