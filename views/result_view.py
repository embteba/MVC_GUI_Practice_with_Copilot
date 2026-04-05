"""
判定結果を表示するView
"""

import streamlit as st
from models.quiz_model import QuizModel
from views.quiz_helper import generate_quiz
from config import QUIZ_DATA_KEY, SUBMITTED_ANSWER_KEY, CURRENT_PAGE_KEY, PAGE_ID_QUIZ


class ResultView:
    """
    判定結果を表示するView。
    
    QuizModelで判定した結果を表示し、
    新しい問題に挑戦するためのボタンを提供します。
    """
    
    def show(self):
        """
        判定結果を表示する。
        """
        if QUIZ_DATA_KEY not in st.session_state or SUBMITTED_ANSWER_KEY not in st.session_state:
            st.warning("データがありません。出題ページから回答を提出してください。")
            return
        
        quiz_data = st.session_state[QUIZ_DATA_KEY]
        user_answer = st.session_state[SUBMITTED_ANSWER_KEY]
        correct_answer = quiz_data['answer']
        
        # 判定結果を取得
        result = QuizModel.judge_answer(correct_answer, user_answer)
        
        # 結果表示
        if result['is_correct']:
            st.success(f"✅ {result['message']}")
        else:
            st.error(f"❌ {result['message']}")
        
        # 詳細情報表示
        st.write(f"**問題**: {quiz_data['num1']} + {quiz_data['num2']} = ?")
        st.write(f"**正解**: {result['correct_answer']}")
        st.write(f"**あなたの回答**: {result['user_answer']}")
        
        # 再チャレンジボタン
        if st.button("新しい問題に挑戦"):
            st.session_state[QUIZ_DATA_KEY] = generate_quiz()
            if SUBMITTED_ANSWER_KEY in st.session_state:
                del st.session_state[SUBMITTED_ANSWER_KEY]
            st.session_state[CURRENT_PAGE_KEY] = PAGE_ID_QUIZ
            st.rerun()
