from bs4 import BeautifulSoup
import base64, os, mimetypes

def embed_resources(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    base_dir = os.path.dirname(html_path)

    # 内嵌 CSS
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href")
        if href and not href.startswith(("http://", "https://")):
            css_path = os.path.join(base_dir, href)
            if os.path.exists(css_path):
                with open(css_path, "r", encoding="utf-8") as css:
                    style_tag = soup.new_tag("style")
                    style_tag.string = css.read()
                    link.replace_with(style_tag)

    # 内嵌图片
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and not src.startswith(("http://", "https://", "data:")):
            img_path = os.path.join(base_dir, src)
            if os.path.exists(img_path):
                mime, _ = mimetypes.guess_type(img_path)
                with open(img_path, "rb") as image:
                    data_uri = f"data:{mime};base64,{base64.b64encode(image.read()).decode()}"
                    img["src"] = data_uri

    output_path = html_path.replace(".html", "_single.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"✅ 已生成独立文件：{output_path}")

embed_resources("./index_tianyongming.html")
