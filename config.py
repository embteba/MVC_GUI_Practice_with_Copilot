"""
アプリケーション共通定数

セッション状態のキーやアプリケーション設定を一元管理します。
"""

# Session State Keys
QUIZ_DATA_KEY = "quiz_data"
SUBMITTED_ANSWER_KEY = "submitted_answer"
CURRENT_PAGE_KEY = "current_page"

# Page IDs
PAGE_ID_QUIZ = "quiz"
PAGE_ID_RESULT = "result"

# Page Labels
PAGE_LABEL_QUIZ = "出題"
PAGE_LABEL_RESULT = "結果"

# Page Titles
PAGE_TITLE_QUIZ = "足し算問題"
PAGE_TITLE_RESULT = "判定結果"

# Quiz Config
QUIZ_MIN_VALUE = 1
QUIZ_MAX_VALUE = 9
QUIZ_INPUT_MIN = 0
QUIZ_INPUT_MAX = 18
