"""
MVC_GUI_Practice_with_Copilot - アプリケーション起点

Streamlitを使用したクイズアプリケーション。
MVCアーキテクチャに基づき、Controllers層と協調してアプリケーションを運行します。

このモジュールはアプリケーション起点のみを担当し、
制御処理はControllers層に委譲します。
"""

from views import configure_page
from controllers.quiz_controller import QuizController


def main():
    """
    メインアプリケーション処理。
    
    ページ設定後、コントローラーにアプリケーション制御を委譲します。
    """
    # ページ設定
    configure_page()
    
    # コントローラーをインスタンス化し、アプリケーション制御を委譲
    controller = QuizController()
    controller.run()


if __name__ == "__main__":
    main()
