import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    return markdown.strip().split("\n")[0].strip()[2:]


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page_html = template.replace("{{ Title }}", title)
    page_html = page_html.replace("{{ Content }}", content_html)
    page_html = page_html.replace('href="/', f'href="{basepath}')
    page_html = page_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "x") as f:
        f.write(page_html)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dir_path_content):
        raise Exception("Source content directory doesn't exist")

    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(source_path):
            dest_path = os.path.splitext(dest_path)[0] + ".html"
            generate_page(source_path, template_path, dest_path, basepath)
        else:
            generate_page_recursive(source_path, template_path, dest_path, basepath)
