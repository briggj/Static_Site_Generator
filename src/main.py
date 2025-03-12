from textnode import TextNode, TextType

def main():
    node = TextNode("Example Text", TextType.ANCHOR_TEXT, "https://example.com")
    print(node)

if __name__ == "__main__":
    main()