import unittest

from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode('What is going on here', TextType.IMAGE, 'www.google.com')
        node2 = TextNode('Just a standard sunday brunch', TextType.IMAGE, 'www.google.com')
        self.assertNotEqual(node, node2)

    def test_one_none(self):
        node = TextNode('This is a text node', TextType.TEXT, 'www.google.com')
        node2 = TextNode('This is a text node', TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_none_none(self):
        node = TextNode('This is a text node', TextType.TEXT, None)
        node2 = TextNode('This is a text node', TextType.TEXT)
        self.assertEqual(node, node2)

    def test_text_type(self):
        node = TextNode('This is a text node', TextType.IMAGE)
        node2 = TextNode('This is a text node', TextType.LINK)
        self.assertNotEqual(node, node2)


if __name__ == '__main__':
    unittest.main()