"""
ページ定義の値オブジェクト
"""


class Page:
    """
    ページ定義を表す値オブジェクト。
    
    ページに関連する情報をカプセル化します。
    
    Attributes:
        label (str): ナビゲーションメニューに表示されるテキスト
        page_id (str): ページを識別する内部ID
        title (str): ページ本体に表示されるタイトル
    """
    
    def __init__(self, label: str, page_id: str, title: str):
        self.label = label
        self.page_id = page_id
        self.title = title
