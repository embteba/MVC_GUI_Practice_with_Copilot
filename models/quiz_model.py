"""
Models層 - 足し算クイズのビジネスロジック

問題の管理と答えの判定を行います。
"""


class QuizModel:
    """
    足し算クイズのビジネスロジックを管理するModel。
    
    ユーザーの回答が正解か判定し、結果を返します。
    """
    
    @staticmethod
    def judge_answer(correct_answer: int, user_answer: int) -> dict:
        """
        ユーザーの回答が正解か判定する。
        
        Args:
            correct_answer (int): 正解
            user_answer (int): ユーザーの回答
        
        Returns:
            dict: {
                'is_correct': bool,
                'correct_answer': int,
                'user_answer': int,
                'message': str
            }
        """
        is_correct = correct_answer == user_answer
        
        return {
            'is_correct': is_correct,
            'correct_answer': correct_answer,
            'user_answer': user_answer,
            'message': '正解です！' if is_correct else '不正解です。'
        }
