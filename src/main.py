from textnode import TextNode, TextType
from htmlnode import HTMLNode
from file_functions import *
from functions import *

def main():
    #move_to_clean('static', 'public', True)
    generate_pages_recursive('content', 'template.html', 'public')


if __name__ == '__main__':
    main()