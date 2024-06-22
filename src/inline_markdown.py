import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        elif len(node.text.split(delimiter)) % 2 == 0:
            raise Exception(
                "Invalid markdown syntax: missing closing delimiter")
        else:
            split_node = node.text.split(delimiter)
            for txt in split_node:
                if f"{delimiter}{txt}{delimiter}" in node.text:
                    new_nodes.append(TextNode(txt, text_type))
                else:
                    new_nodes.append(TextNode(txt, text_type_text))

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        old_text = old_node.text
        # list of tuples: (alt text, url)
        images = extract_markdown_images(old_text)
        if len(images) == 0:    # if no images, append entire node
            new_nodes.append(old_node)
            continue
        for image in images:
            # text sections that are not images
            sections = old_text.split(f"![{image[0]}]({image[1]})")
            if len(sections) != 2:
                raise ValueError("Unclosed image")
            if sections[0] != "":
                # append first text section
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(   # append image
                TextNode(
                    image[0],
                    text_type_image,
                    image[1]
                )
            )
            old_text = sections[1]
        if old_text != "":
            # append the rest of the text
            new_nodes.append(TextNode(old_text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        old_text = old_node.text
        # list of tuples: (alt text, url)
        links = extract_markdown_links(old_text)
        if len(links) == 0:    # if no links, append entire node
            new_nodes.append(old_node)
            continue
        for link in links:
            # text sections that are not links
            sections = old_text.split(f"[{link[0]}]({link[1]})")
            if len(sections) != 2:
                raise ValueError("Unclosed link")
            if sections[0] != "":
                # append first text section
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(   # append link
                TextNode(
                    link[0],
                    text_type_link,
                    link[1]
                )
            )
            old_text = sections[1]
        if old_text != "":
            # append the rest of the text
            new_nodes.append(TextNode(old_text, text_type_text))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, '**', text_type_bold)
    nodes = split_nodes_delimiter(nodes, '*', text_type_italic)
    nodes = split_nodes_delimiter(nodes, '`', text_type_code)
    nodes = split_nodes_link(split_nodes_image(nodes))
    return nodes
