import unittest
from functions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_text_nodes, markdown_to_blocks, block_to_block_type, text_to_children, block_stripper, markdown_to_html_node
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_types import BlockType
import re

class TestTextToNode(unittest.TestCase):

    
    def test_exception_attribute(self):
        with self.assertRaises(AttributeError):
            node = TextNode("We want an exception", TextType.PORN)
            text_node_to_html_node(node)

    def test_exception_type_not_supported(self):
        node = TextNode('We want an exception', 'This is not a text type')
        with self.assertRaises(Exception) as e:
            text_node_to_html_node(node)
        self.assertEqual(str(e.exception), 'Text Type not supported')

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("this is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'this is a bold node')

    def test_image(self):
        node = TextNode('Image of a cat', TextType.IMAGE, url='www.google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {'src':'www.google.com', 'alt':'Image of a cat'})

    def test_image_no_alt(self):
        node = TextNode(None, TextType.IMAGE, url='www.google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {'src':'www.google.com', 'alt':''})


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_no_changes(self):
        node = TextNode("We have no changes to make to this string", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)
        self.assertIn(TextNode('We have no changes to make to this string', TextType.TEXT), new_nodes)
        self.assertEqual(1, len(new_nodes))

    def test_exceptions_no_closing_delim(self):
        node = TextNode("Here there is 'no closing delimiter for the code block", TextType.TEXT)
        with self.assertRaises(Exception) as e:
            new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)
        self.assertEqual(str(e.exception), 'Closing delimiter not found')

    def test_multiple_blocks(self):
        node = TextNode("Here there are'two' seperate 'code blocks for' our function to parse", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)
        self.assertIn(TextNode('two', TextType.CODE), new_nodes)
        self.assertIn(TextNode(' seperate ', TextType.TEXT), new_nodes)
        self.assertIn(TextNode('code blocks for', TextType.CODE), new_nodes)

    def test_multiple_old_nodes(self):
        nodes = [
            TextNode("Here is node **1** to split", TextType.TEXT),
            TextNode('Node 2 does not have any bold text', TextType.TEXT),
            TextNode('Node **3** has **multiple** blocks of bold text to split',TextType.BOLD)
        ]
        new_nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertIn(TextNode('1', TextType.BOLD), new_nodes)

    def test_delim_char_outside_delim(self):
        nodes = [
            TextNode('Here is the problematic* string in our nodes', TextType.TEXT),
            TextNode('This string is problematic* for a **different** reason', TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertIn(TextNode('different', TextType.BOLD), new_nodes)
        self.assertIn(TextNode('Here is the problematic* string in our nodes',TextType.TEXT), new_nodes)
        self.assertIn(TextNode('This string is problematic* for a ', TextType.TEXT), new_nodes)

    def test_nontext_type(self):
        nodes = [
            TextNode("Here is node **1** to split", TextType.TEXT),
            TextNode('Node 2 does not have any bold text', TextType.TEXT),
            TextNode('Node **3** has **multiple** blocks of bold text to split',TextType.BOLD),
            TextNode('This is the crucial node here', TextType.ITALIC)
        ]
        new_nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertIn(TextNode('This is the crucial node here', TextType.ITALIC), new_nodes)


class TestExtractMarkdownImages(unittest.TestCase):
        
    def test_base(self):
        result = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(result,[("rick roll", "https://i.imgur.com/aKaOqIh.gif"),("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_base_links(self):
        result = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

class TestSplitNodesLink(unittest.TestCase):
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            'This is text with a [link](www.google.com) and another [second link](www.yahoo.com)',
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode('This is text with a ', TextType.TEXT),
                TextNode('link', TextType.LINK, 'www.google.com'),
                TextNode(' and another ', TextType.TEXT),
                TextNode('second link', TextType.LINK, 'www.yahoo.com')
            ],
            new_nodes
        )

    def test_image_at_end(self):
        node = [TextNode(
            'This is text with the image at the end ![image](www.google.com)', TextType.TEXT
        )]
        new_nodes = split_nodes_image(node)
        self.assertEqual(
            [
                TextNode('This is text with the image at the end ', TextType.TEXT),
                TextNode('image', TextType.IMAGE, 'www.google.com')
            ],
            new_nodes
        )


    def test_link_at_start(self):
        node = [TextNode(
            '[google](www.google.com) is the most used search engine', TextType.TEXT
        )]
        new_node = split_nodes_link(node)
        self.assertEqual(
            [
                TextNode('google', TextType.LINK, 'www.google.com'),
                TextNode(' is the most used search engine', TextType.TEXT)
            ],
            new_node
        )

class TestTextToTextNodes(unittest.TestCase):

    def test_base(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        text_nodes = text_to_text_nodes(text)
        self.assertEqual(text_nodes,
                         [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://boot.dev"),
                         ]
                         )
        
    def test_overlap_bold_wins_inside_italic(self):
        text = "_**x**_"
        with self.assertRaises(Exception) as e:
            nodes = text_to_text_nodes(text)
        self.assertEqual(str(e.exception), 'Closing delimiter not found')

    def test_code_protects_inner_symbols(self):
        text = "`a **b** _c_`"
        nodes = text_to_text_nodes(text)
        self.assertEqual(
            nodes,
            [TextNode("a **b** _c_", TextType.CODE)]
        )        

    def test_no_closing_delim(self):
        text = 'Hi mom** this should be an exception raised'
        with self.assertRaises(Exception) as e:
            nodes = text_to_text_nodes(text)
        self.assertEqual(str(e.exception), 'Closing delimiter not found') 

class TestMarkdownToBlocks(unittest.TestCase):
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_leading_trailing_empty_strings(self):
        md = """

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_multiple_line_breaks(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_md(self):
        md = ''
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_only_whitespaces(self):
        md = """



"""
        blocks  = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

class TestBlockType(unittest.TestCase):
    def test_ordered_list(self):
        block = '1. a\n2. b\n3. c'
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = 'This is just a paragraph'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = '- a\n- b'
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_code(self):
        block = '``` this is fancy code \n I am so good at coding ```'
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_heading(self):
        block = '#### This is a heading block'
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_missing_space_hash(self):
        block = '##Oops we are missing a space - paragraph now'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_no_closing_ticks(self):
        block = '``` Oh no I forgot to close this'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_closed_early(self):
        block = '```Oops, closed``` too early'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_not_start(self):
        block = 'Ooops ``` we started the code block too late```'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_missing_middle_elements(self):
        block = '- element 1\nelement 2\n- element 3'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_incorrect_order(self):
        block = '1. this list\n3. is missing\n4. the number 2'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
###### This is a h6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h6>This is a h6</h6></div>'
        )

    def test_heading_too_many_hashes_raises(self):
        md = "####### Too many"
        print(block_to_block_type('####### Too many'))
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)

if __name__ == "__main__":
    unittest.main()