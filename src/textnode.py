from enum import Enum

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold text'
    ITALIC = 'italic text'
    CODE  = 'code text'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, external_text_node):
        if self.text == external_text_node.text and self.text_type == external_text_node.text_type and self.url == external_text_node.url:
            return True
        return False
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
    
    