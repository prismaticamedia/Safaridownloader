from lxml import html
import re

html_content = """
<div id="sbo-rt-content">
  <p>Some text</p>
  <img src="https://learning.oreilly.com/api/v2/epubs/urn:orm:book:12345/files/images/test.png">
  <img src="images/test2.jpg">
  <img src="graphics/test3.gif">
  <img src="test4.png">
  <img src="https://learning.oreilly.com/library/view/book/123/images/test5.jpg">
</div>
"""

root = html.fromstring(html_content, base_url="https://learning.oreilly.com")
book_content = root.xpath("//div[@id='sbo-rt-content']")[0]

extracted_images = []
def link_replace(link):
    print("Found link:", link)
    if link and not link.startswith("mailto"):
        if any(x in link for x in ["cover", "images", "graphics"]) or link.endswith((".jpg", ".png", ".gif", ".jpeg")):
            image = link.split("/")[-1]
            extracted_images.append(link)
            print("  -> Matched as image:", image)
            return "Images/" + image
    return link

book_content.rewrite_links(link_replace)
print("Extracted:", extracted_images)
