"""
クイズ共通処理

問題生成などの共通ロジックを集約します。
"""

import random
from config import QUIZ_MIN_VALUE, QUIZ_MAX_VALUE


def generate_quiz() -> dict:
    """
    足し算問題を生成する。
    
    Returns:
        dict: {
            'num1': int,
            'num2': int,
            'answer': int
        }
    """
    num1 = random.randint(QUIZ_MIN_VALUE, QUIZ_MAX_VALUE)
    num2 = random.randint(QUIZ_MIN_VALUE, QUIZ_MAX_VALUE)
    return {
        'num1': num1,
        'num2': num2,
        'answer': num1 + num2
    }
