# test_htmlnode.py
# Test cases for HTMLNode, LeafNode, and ParentNode classes
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode("p")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode("a", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_different_prop_types(self):
        node = HTMLNode("div", props={"id": "my-div", "data-count": 10})
        self.assertEqual(node.props_to_html(), ' id="my-div" data-count="10"')

    def test_eq_different_props(self):
        node1 = HTMLNode("div",props={"id":"1"})
        node2 = HTMLNode("div",props={"id":"2"})
        self.assertNotEqual(node1,node2)

    def test_eq_same_props(self):
        node1 = HTMLNode("div",props={"id":"1"})
        node2 = HTMLNode("div",props={"id":"1"})
        self.assertEqual(node1,node2)

    def test_eq_different_tags(self):
        node1 = HTMLNode("div",props={"id":"1"})
        node2 = HTMLNode("p",props={"id":"1"})
        self.assertNotEqual(node1,node2)

    def test_eq_different_values(self):
        node1 = HTMLNode("div",value="1")
        node2 = HTMLNode("div",value="2")
        self.assertNotEqual(node1,node2)

    def test_eq_different_children(self):
        node1 = HTMLNode("div", children=[HTMLNode("p", value="test1")])
        node2 = HTMLNode("div", children=[HTMLNode("a", value="test2")])
        self.assertNotEqual(node1, node2)

    def test_eq_same_children(self):
        child = HTMLNode("p", value="test")
        node1 = HTMLNode("div", children=[child])
        node2 = HTMLNode("div", children=[child])
        self.assertEqual(node1, node2)

    def test_eq_none_children(self):
        node1 = HTMLNode("div")
        node2 = HTMLNode("div", children = [])
        self.assertEqual(node1, node2)

    def test_eq_none_props(self):
        node1 = HTMLNode("div")
        node2 = HTMLNode("div", props = {})
        self.assertEqual(node1,node2)
    def test_eq_none_value(self):
        node1 = HTMLNode("div")
        node2 = HTMLNode("div", value = None)
        self.assertEqual(node1,node2)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "My Heading")
        self.assertEqual(node.to_html(), "<h1>My Heading</h1>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_leaf_to_html_empty_props(self):
        node = LeafNode("span", "Just text", {})
        self.assertEqual(node.to_html(), "<span>Just text</span>")

    def test_leaf_to_html_raises_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("em", "child2")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><span>child1</span><em>child2</em></div>")

    def test_to_html_nested_parent_nodes(self):
        inner_parent = ParentNode("ul", [LeafNode("li", "item1"), LeafNode("li", "item2")])
        outer_parent = ParentNode("div", [inner_parent])
        self.assertEqual(outer_parent.to_html(), "<div><ul><li>item1</li><li>item2</li></ul></div>")

    def test_to_html_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "container", "id": "main"})
        self.assertEqual(parent.to_html(), '<div class="container" id="main"><span>child</span></div>')

    def test_to_html_raises_value_error_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p","test")]).to_html()

    def test_to_html_raises_value_error_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_parent_node_children_are_htmlnode(self):
        child = HTMLNode("p", "test")
        node = ParentNode("div", [child])
        self.assertEqual(node.to_html(), "<div><p>test</p></div>")

    def test_parent_node_children_are_htmlnode(self):
        child = LeafNode("p", "test") # changed to LeafNode
        node = ParentNode("div", [child])
        self.assertEqual(node.to_html(), "<div><p>test</p></div>")