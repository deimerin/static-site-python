import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links, extract_title

class TestExtractMarkdown(unittest.TestCase):
    
    def test_images(self):
        img1 = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        img2 = "Multiple ![first](url1.jpg) and ![second](url2.png) images"
        img3 = "![alt text with spaces](https://example.com/image.gif)"
        img4 = "No images here, just text"
        img5 = "![](empty-alt.jpg)"

        self.assertEqual(extract_markdown_images(img1), [("image", "https://i.imgur.com/zjjcJKZ.png")])
        self.assertEqual(extract_markdown_images(img2), [("first", "url1.jpg"), ("second", "url2.png")])
        self.assertEqual(extract_markdown_images(img3), [("alt text with spaces", "https://example.com/image.gif")])
        self.assertEqual(extract_markdown_images(img4), [])
        self.assertEqual(extract_markdown_images(img5), [("", "empty-alt.jpg")])

    def test_links(self):
        lnk1 = "This is text with a [link](https://www.boot.dev)"
        lnk2 = "Multiple [first link](url1.com) and [second link](url2.org) here"
        lnk3 = "[link with spaces](https://example.com/page)"
        lnk4 = "No links in this string"
        lnk5 = "[](empty-text.com)"

        self.assertEqual(extract_markdown_links(lnk1), [("link", "https://www.boot.dev")])
        self.assertEqual(extract_markdown_links(lnk2), [("first link", "url1.com"), ("second link", "url2.org")])
        self.assertEqual(extract_markdown_links(lnk3), [("link with spaces", "https://example.com/page")])
        self.assertEqual(extract_markdown_links(lnk4), [])
        self.assertEqual(extract_markdown_links(lnk5), [("", "empty-text.com")])

    def test_mixed_content(self):
        mx1 = "This has an ![image](img.jpg) and a [link](site.com)"
        mx2 = "![img1](url1.jpg) then [link1](site1.com) then ![img2](url2.png)"
        mx3 = "Text with [link](site.com) and ![image](pic.jpg) mixed together"

        self.assertEqual(extract_markdown_images(mx1), [("image", "img.jpg")])
        self.assertEqual(extract_markdown_links(mx1), [("link", "site.com")])

        self.assertEqual(extract_markdown_images(mx2), [("img1", "url1.jpg"), ("img2", "url2.png")])
        self.assertEqual(extract_markdown_links(mx3), [("link", "site.com")])


    def test_extract_title(self):
        # Single title at the start
        md1 = "# My Title\nSome content here."
        self.assertEqual(extract_title(md1), "My Title")

        # Title with leading/trailing spaces
        md2 = "#    Another Title   \nMore text."
        self.assertEqual(extract_title(md2), "Another Title")

        # Multiple titles in the markdown
        md3 = "# First Title\nSome text\n## Second Title\nMore text"
        self.assertEqual(extract_title(md3), "First Title")

        # Title not at the beginning
        md4 = "Intro text\n# Title After Text\nContent"
        self.assertEqual(extract_title(md4), "Title After Text")

        # No title present should raise Exception
        md5 = "No title here\nJust text"
        with self.assertRaises(Exception):
            extract_title(md5)

        # Title with special characters
        md6 = "# T!t1e @ 2024\nContent"
        self.assertEqual(extract_title(md6), "T!t1e @ 2024")

        # Title with only hash and space
        md7 = "# \nContent"
        self.assertEqual(extract_title(md7), "")
        
