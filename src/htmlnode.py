

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = [] if children is None else children
        self.props = {} if props is None else props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        output = ''
        for i in self.props:
            output = output + f' {i}="{self.props[i]}"'
        return output
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    
    def __eq__(self, node2):
        if self.tag == node2.tag and self.value == node2.value and self.children == node2.children and self.props == node2.props:
            return True
        return False

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        #super().__init__(tag , value, None, props)
        #alternatively if we did not want to rely on positional args:
        super().__init__(tag = tag, value = value, children = None, props = props)



    def to_html(self):
        if self.value == None:
            raise ValueError('Leaf Node missing Value')
        if self.tag == None:
            return self.value
        else:
            if self.props is None:
                return f'<{self.tag}>{self.value}</{self.tag}>'
            else:
                return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag = tag, children = children, props = props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if not self.children:
            raise ValueError('Parent Node has no Children')
        #Recursive string - return the html tag of the node and its children respecting props
        conc_child = ''
        for i in self.children:
            conc_child = conc_child + i.to_html()
        if self.props is None:
            out_string = f'<{self.tag}>{conc_child}</{self.tag}>'
        else:
            return f'<{self.tag}{self.props_to_html()}>{conc_child}</{self.tag}>'
        return out_string

