from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    mynode = TextNode('This is some anchor text', TextType.LINK, 'www.boot.dev')
    myhtmlnode = HTMLNode()
    myhtmlnode2 = HTMLNode("p", 'Hi mom, I am coding!', None, None)
    print(mynode)
    print(myhtmlnode)
    print(myhtmlnode2)


if __name__ == '__main__':
    main()