import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from block_types import BlockType

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception('Text Type not supported')
    leaf_node = LeafNode(tag = None, value = text_node.text, props = None)


    if text_node.text_type == TextType.BOLD:
        leaf_node.tag = 'b'

    if text_node.text_type == TextType.ITALIC:
        leaf_node.tag = 'i'

    if text_node.text_type == TextType.CODE:
        leaf_node.tag = 'code'

    if text_node.text_type == TextType.LINK:
        leaf_node.tag = 'a'
        #We currently do not have anchor text from TextNode so I am not sure what to do here.
        #I think value = text_node.text takes care of this for us
        leaf_node.props = {'href': text_node.url}

    #This is the other case I am not 100% sure on - my main concern is what if url==None
    #If url == None, then the props still has an entry that will print to the HTML file I think
    if text_node.text_type == TextType.IMAGE:
        leaf_node.tag = 'img'
        leaf_node.value = ''
        leaf_node.props = {'src':text_node.url, 'alt':text_node.text or ''}

    return leaf_node


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
        switch = 0
        new_node_string = ''
        delim_string = ''
        for j in node.text:
            if j in delimiter:
                delim_string += j
                if len(delim_string) == len(delimiter) and delim_string != delimiter:
                    new_node_string += delim_string[0]
                    delim_string = delim_string[1:]
                if delim_string == delimiter:

                    if switch == 0:
                        new_node = TextNode(new_node_string, TextType.TEXT)
                        switch = 1
                        new_node_string = ''
                        node_list.append(new_node)
                        delim_string = ''
                    elif switch == 1:
                        new_node = TextNode(new_node_string, text_type)
                        switch = 0
                        new_node_string = ''
                        node_list.append(new_node)
                        delim_string = ''
            else:
                new_node_string += delim_string + j
                delim_string = ''
        if delim_string != '':
            new_node_string += delim_string
        if new_node_string != '':
            new_node = TextNode(new_node_string, TextType.TEXT)
            node_list.append(new_node)
        if switch == 1:
            raise Exception('Closing delimiter not found')
    return node_list
    

def extract_markdown_images(text):
    tuple_list = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    #Example: ![Alt text](https://www.google.com)
    return tuple_list

def extract_markdown_links(text):
    tuple_list = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return tuple_list

def split_nodes_link(old_nodes):
    #This accepts textnodes and gives new text nodes
    #First we will use extract the links:
    new_nodes = []
    for i in old_nodes:
        if i.text_type != TextType.TEXT:
            new_nodes.append(i)
            continue
        old_text = i.text
        links = extract_markdown_links(old_text)
        text_list = [old_text]
        for k in links:
            anchor_text = k[0]
            href = k[1]
            delim = f'[{anchor_text}]({href})'
            new_text = []
            for j in text_list:
                split_text = j.split(delim, 1)
                if delim in j:
                    if len(split_text)==1:
                        new_text.extend([split_text[0], delim])
                    else:
                        new_text.extend([split_text[0], delim, split_text[1]])
                else:
                    new_text.append(j)
            text_list = new_text
        #We now have a text_list that is a list of text items and delims in order - time to make them nodes
        delim_list = []
        for link in links:
            delim_list.append(f'[{link[0]}]({link[1]})')
        for item in text_list:
            if item in delim_list:
                tuple_list = extract_markdown_links(item)
                anchor = tuple_list[0][0]
                href = tuple_list[0][1]
                node = TextNode(anchor, TextType.LINK, href)
                new_nodes.append(node)
            elif item != '':
                node = TextNode(item, TextType.TEXT)
                new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    #This accepts textnodes and gives new text nodes
    #First we will use extract the links:
    new_nodes = []
    for i in old_nodes:
        if i.text_type != TextType.TEXT:
            new_nodes.append(i)
            continue
        old_text = i.text
        links = extract_markdown_images(old_text)
        text_list = [old_text]
        for k in links:
            image_alt = k[0]
            image_link = k[1]
            delim = f'![{image_alt}]({image_link})'
            new_text = []
            for j in text_list:
                split_text = j.split(delim, 1)
                if delim in j:
                    #This first part of the if statement is likely unecessary - split creates '' on the side of the delim with no text
                    if len(split_text)==1:
                        new_text.extend([split_text[0], delim])
                    else:
                        new_text.extend([split_text[0], delim, split_text[1]])
                else:
                    new_text.append(j)
            text_list = new_text
        #We now have a text_list that is a list of text items and delims in order - time to make them nodes
        delim_list = []
        for link in links:
            delim_list.append(f'![{link[0]}]({link[1]})')
        for item in text_list:
            if item in delim_list:
                tuple_list = extract_markdown_images(item)
                alt = tuple_list[0][0]
                url = tuple_list[0][1]
                node = TextNode(alt, TextType.IMAGE, url)
                new_nodes.append(node)
            elif item != '':
                node = TextNode(item, TextType.TEXT)
                new_nodes.append(node)
    return new_nodes


def text_to_text_nodes(text):
    text_node = TextNode(text, TextType.TEXT)
    
    #dictionaries are not stable in the order we access the contents so we will build a stable function
    #delim_dict = {'**':TextType.BOLD, '_':TextType.ITALIC, "`":TextType.CODE}
    
    new_nodes = split_nodes_link([text_node])
    new_nodes = split_nodes_image(new_nodes)
    
    #This was from the initial pass where the order of splitting was not deterministic
    #for delim in delim_dict:
    #    new_nodes = split_nodes_delimiter(new_nodes, delim, delim_dict[delim])

    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)

    return new_nodes


def markdown_to_blocks(markdown):
    block_list = markdown.split('\n\n')
    updated_block_list = []
    for i in range(0, len(block_list)):
        if block_list[i].strip() != '':
            updated_block_list.append(block_list[i].strip())
    return updated_block_list
        

def block_to_block_type(block):
    if re.match(r'#{1,6} ',block):
        return BlockType.HEADING
    
    if re.search(r'\A```.*```\Z',block,re.DOTALL):
        return BlockType.CODE
    
    #The rest of the block types require checks over lines:
    line_list = block.split('\n')

    #quote block
    for i in range(0,len(line_list)):
        if re.match(r'>',line_list[i]):
            if i == len(line_list)-1:
                return BlockType.QUOTE
        else:
            break
    
    #unordered list
    for i in range(0, len(line_list)):
        if re.match(r'- ',line_list[i]):
            if i ==len(line_list)-1:
                return BlockType.UNORDERED_LIST
        else:
            break
    
    #ordered list
    for i in range(0, len(line_list)):
        num = i + 1
        if re.match(fr'{num}\. ', line_list[i]):
            if i == len(line_list)-1:
                return BlockType.ORDERED_LIST
        else:
            break
    return BlockType.PARAGRAPH

def text_to_children(text, block_type):
    cleaned_text = text[0] #Remember we are feeding in the touple (textblock/list, level)
    #In the case of unordered or ordered lists, the text we pass is a list of items:
    if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
        li_children = []
        for i in cleaned_text:
            text_nodes = text_to_text_nodes(i)
            children_nodes = [text_node_to_html_node(node) for node in text_nodes]
            li_children.append(HTMLNode(tag='li', children = children_nodes))
        #Now we need to build the parent of the children list items
        child_node = HTMLNode(tag = ('ul' if block_type == BlockType.UNORDERED_LIST else 'ol'),
                              children = li_children)
        return child_node
    else:
        text_nodes = text_to_text_nodes(cleaned_text)
        #Now we generate the tags
        if block_type == BlockType.HEADING:
            heading_level = text[1]
            node_tag = f'h{heading_level}'
        elif block_type == BlockType.PARAGRAPH:
            node_tag = 'p'
        elif block_type == BlockType.QUOTE:
            node_tag = 'blockquote'
        else:
            raise ValueError('Unhandled block type exception')
        children_nodes = [text_node_to_html_node(node) for node in text_nodes]
        child_node = HTMLNode( tag = node_tag, children = children_nodes)
        return child_node

def block_stripper(text, block_type):
    level = None
    if block_type == BlockType.HEADING:
        heading_count = 0
        for i in text:
            if i == '#':
                heading_count += 1
            else:
                break
        if heading_count not in range(1,7):
            raise ValueError('Heading delimiter outside range')
        if heading_count >= len(text) or text[heading_count] != ' ':
            raise ValueError('Missing space after heading hashes')
        cleaned_text = text[heading_count+1:]
        if cleaned_text.strip() == '':
            raise ValueError('Empty heading')
        level = heading_count
        return cleaned_text, level
    if block_type == BlockType.QUOTE:
        uncleaned_text = text.split('\n')
        cleaned_text_list = []
        for item in uncleaned_text:
            if item.startswith('> '):
                cleaned_item = item[2:]
                cleaned_text_list.append(cleaned_item)
            else:
                if item != '':
                    raise ValueError('Quote block contains non-quote in markdown')
        cleaned_text = '\n'.join(cleaned_text_list)
        return cleaned_text, level
    if block_type == BlockType.UNORDERED_LIST:
        uncleaned_text = text.split('\n')
        cleaned_text = []
        for item in uncleaned_text:
            if item.startswith('- '):
                cleaned_item = item[2:]
                cleaned_text.append(cleaned_item)
            else:
                if item != '':
                    raise ValueError('Unordered list block contains non-list item in markdown')
        return cleaned_text, level
    if block_type == BlockType.ORDERED_LIST:
        uncleaned_text = text.split('\n')
        cleaned_text = []
        level = 1
        for item in uncleaned_text:
            if item.startswith(f'{level}. '):
                prefix = f'{level}. '
                cleaned_item = item[len(prefix):]
                cleaned_text.append(cleaned_item)
                level += 1
            elif item == '':
                continue
            else:
                raise ValueError('Ordered list block contains non-list item in markdown')
        level -= 1
        return cleaned_text, level
    return text, level

def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    master_list = []
    for block in block_list:
        block_type = block_to_block_type(block)
        node_value = None
        children_list = []
        node_tag = None
        if block_type == BlockType.CODE:
            node_tag = 'pre'
            stripped_block = block.strip('```')
            stripped_block.strip('\n')
            code_child = HTMLNode(tag = 'code', value = stripped_block, children = None)
            children_list = [code_child]
        else:


        block_node = HTMLNode(tag = node_tag, value = node_value, children = children_list)
        master_list.append(block_node)
    master_node = HTMLNode(tag = 'div', children = master_list)
    return master_node