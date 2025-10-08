import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_basecase(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_tag_case(self):
        node = HTMLNode(tag = 'p')
        node2 = HTMLNode(tag = '<a>')
        self.assertNotEqual(node, node2)
    
    def test_value_case(self):
        node = HTMLNode(value = 'Hi mom, I am coding!')
        node2 = HTMLNode(value = 'Hi dad, I am coding!')
        self.assertNotEqual(node, node2)
    
    def test_props_case(self):
        node = HTMLNode(props = {'href': 'https://www.google.com'})
        node2 = HTMLNode(props = {'target': '_blank'})
        self.assertNotEqual(node, node2)

    def test_mixed_case(self):
        node = HTMLNode(tag = 'p')
        node2 = HTMLNode(value = 'p')
        self.assertNotEqual(node, node2)

    def test_mixed_equal(self):
        node = HTMLNode(tag = 'p', value = 'Hi mom, I am coding!')
        node2 = HTMLNode(tag = 'p', value = 'Hi mom, I am coding!')
        self.assertEqual(node, node2)

class TestHTMLChildren(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode(tag = "p", value = "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_img(self):
        node = LeafNode(
            "img",
            "",
            {"src": "https://example.com/cat.png", "alt": "A cat", "width": "200"},
        )
        self.assertEqual(
            node.to_html(),
            '<img src="https://example.com/cat.png" alt="A cat" width="200"></img>',
        )

    def test_leaf_to_html_link(self):
        node = LeafNode(
            'a',
            'Click me',
            {'href': 'www.google.com', 'target': '_blank'}
        )
        self.assertEqual(node.to_html(),
                         '<a href="www.google.com" target="_blank">Click me</a>')
    
    def test_value_none_exception(self):
        node = LeafNode(tag = 'p', value = None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestHTMLParent(unittest.TestCase):
    def test_tag_none_exception(self):
        node = ParentNode(tag = None, children = [
            LeafNode('b', 'bold text'),
            LeafNode(None, 'normal text'),
            LeafNode('i', 'italic text'),
            LeafNode(None, 'normal text')
        ])
        with self.assertRaises(ValueError) as e:
            node.to_html()

    def test_child_value_none_exception(self):
        node = ParentNode(tag = 'p', children = [
            LeafNode('b', 'bold text'),
            LeafNode(None, 'normal text'),
            LeafNode('i', 'italic text'),
            LeafNode(None, 'normal text'),
            LeafNode(tag = None, value = None)
        ])
        with self.assertRaises(ValueError) as e:
            node.to_html()
        self.assertEqual(str(e.exception), 'Leaf Node missing Value')

    def test_no_children_exception(self):
        node = ParentNode(tag = 'p', children = None)
        with self.assertRaises(ValueError) as e:
            node.to_html()
        self.assertEqual(str(e.exception), 'Parent Node has no Children')

    def test_base_case(self):
        node = ParentNode(tag = 'p', children = [
            LeafNode('b', 'bold text'),
            LeafNode(None, 'normal text'),
            LeafNode('i', 'italic text'),
            LeafNode(None, 'normal text')
        ])
        self.assertEqual(node.to_html(),
                         '<p><b>bold text</b>normal text<i>italic text</i>normal text</p>'
                         )
        
    def test_nested_parent(self):
        node2 = ParentNode(tag = 'i', children = [
            LeafNode('b', 'bold text'),
            LeafNode(None, 'italic text'),
            LeafNode('b', 'bold text')
        ])
        node = ParentNode(tag = 'p', children = [
            node2,
            LeafNode(None, 'normal text')
        ])

        self.assertEqual(node.to_html(), 
                         '<p><i><b>bold text</b>italic text<b>bold text</b></i>normal text</p>')

    def test_nested_with_props(self):
        int_node = ParentNode(tag = 'i', children = [
            LeafNode('b', 'bold text'),
            LeafNode(None, 'italic text'),
            LeafNode('b', 'bold text'),
            LeafNode(
            "img",
            "",
            {"src": "https://example.com/cat.png", "alt": "A cat", "width": "200"},
        )
        ])
        node = ParentNode(tag = 'p', children = [
            int_node,
            LeafNode(None, 'normal text')
        ], props = {'id':'tagline',
                    'color':'red'})
        self.assertEqual(node.to_html(),
                         '<p id="tagline" color="red"><i><b>bold text</b>italic text<b>bold text</b><img src="https://example.com/cat.png" alt="A cat" width="200"></img></i>normal text</p>')

if __name__ == "__main__":
    unittest.main()