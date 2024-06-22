import os
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_heading,
    markdown_to_html_node
)


def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No h1 header")


def generate_page(src_path, template_path, dst_path):
    print(f" * {src_path} {template_path} -> {dst_path}")
    with open(src_path) as src:
        src_contents = src.read()
    with open(template_path) as template:
        page_contents = template.read()

    node = markdown_to_html_node(src_contents)
    html_title = extract_title(src_contents)
    html_content = node.to_html()

    page_contents = page_contents.replace("{{ Title }}", html_title)
    page_contents = page_contents.replace("{{ Content }}", html_content)

    dst_dir_path = os.path.dirname(dst_path)
    if dst_dir_path != "":
        os.makedirs(dst_dir_path, exist_ok=True)
    with open(dst_path, 'w') as dst:
        dst.write(page_contents)


def generate_pages_recursive(src_path, template_path, dst_dir_path):
    content = os.listdir(src_path)
    for node in content:
        node_path = os.path.join(src_path, node)
        dst_path = os.path.join(dst_dir_path, node)
        if os.path.isfile(node_path):
            if node_path.endswith(".md"):
                generate_page(node_path, template_path,
                              dst_path.replace(".md", ".html"))
        else:
            generate_pages_recursive(
                node_path,
                template_path,
                dst_path
            )
