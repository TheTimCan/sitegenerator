import os
import shutil
from generate_page import generate_pages_recursive

dir_static = "./static"
dir_public = "./public"
dir_content = "./content"
template_path = "./template.html"


def main():
    if os.path.exists(dir_public):
        shutil.rmtree(dir_public)
    copy_static_to_public(dir_static, dir_public)
    print("Generating page...")
    generate_pages_recursive('./content', './template.html', './public')


def copy_static_to_public(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    static_dir = os.listdir(src)
    if len(static_dir) > 0:
        for node in static_dir:
            node_path = os.path.join(src, node)
            dst_path = os.path.join(dst, node)
            if os.path.isfile(node_path):
                shutil.copy(node_path, dst_path)
            else:
                os.mkdir(dst_path)
                copy_static_to_public(node_path, dst_path)


main()
