from textnode import TextNode, TextType
from htmlnode import HTMLNode
from file_functions import *

def main():
    mynode = TextNode('This is some anchor text', TextType.LINK, 'www.boot.dev')
    myhtmlnode = HTMLNode()
    myhtmlnode2 = HTMLNode("p", 'Hi mom, I am coding!', None, None)
    print(mynode)
    print(myhtmlnode)
    print(myhtmlnode2)

    #I am not sure what my current working directory is.  It should be ../static_web/
    move_to_clean('static', 'public', True)

if __name__ == '__main__':
    main()