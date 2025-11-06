from textnode import TextNode, TextType
from htmlnode import HTMLNode
from file_functions import *
from functions import *
import sys

def main():
    if len(sys.argv)<2:
        basepath = '/'
    elif sys.argv[1]:
        basepath = sys.argv[1]
    else:
        raise Exception('Unexpected error occurred')
    
    move_to_clean('static', 'public', True)
    generate_pages_recursive('content', 'template.html', 'public', basepath)



if __name__ == '__main__':
    main()