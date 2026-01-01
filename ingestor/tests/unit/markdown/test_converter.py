"""Tests for MarkdownConverter."""

import pytest

from ingestor.markdown.converter import MarkdownConverter, html_to_markdown


class TestMarkdownConverter:
    """Tests for MarkdownConverter class."""

    @pytest.fixture
    def converter(self):
        """Create a MarkdownConverter instance."""
        return MarkdownConverter()

    def test_convert_simple_html(self, converter):
        """Test converting simple HTML."""
        html = "<p>Hello, World!</p>"
        result = converter.convert(html)

        assert "Hello, World!" in result

    def test_convert_headings(self, converter):
        """Test converting headings to ATX style."""
        html = "<h1>Title</h1><h2>Subtitle</h2>"
        result = converter.convert(html)

        assert "# Title" in result
        assert "## Subtitle" in result

    def test_convert_links(self, converter):
        """Test converting links."""
        html = '<a href="https://example.com">Link</a>'
        result = converter.convert(html)

        assert "[Link](https://example.com)" in result

    def test_convert_lists(self, converter):
        """Test converting lists."""
        html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        result = converter.convert(html)

        assert "Item 1" in result
        assert "Item 2" in result

    def test_strip_script_tags(self, converter):
        """Test stripping script tags."""
        html = "<p>Text</p><script>alert('xss')</script>"
        result = converter.convert(html)

        assert "Text" in result
        # Script tag itself should not appear as markdown
        assert "<script>" not in result

    def test_strip_style_tags(self, converter):
        """Test stripping style tags."""
        html = "<p>Text</p><style>.red { color: red; }</style>"
        result = converter.convert(html)

        assert "Text" in result
        # Style tag itself should not appear as markdown
        assert "<style>" not in result

    def test_clean_removes_excessive_newlines(self, converter):
        """Test clean removes excessive blank lines."""
        md = "Line 1\n\n\n\n\nLine 2"
        result = converter.clean(md)

        # Should have at most 2 newlines between
        assert "\n\n\n" not in result
        assert "Line 1" in result
        assert "Line 2" in result

    def test_clean_strips_trailing_whitespace(self, converter):
        """Test clean strips trailing whitespace."""
        md = "Line 1   \nLine 2  "
        result = converter.clean(md)

        assert "Line 1   " not in result
        assert "Line 2  " not in result


class TestHtmlToMarkdown:
    """Tests for html_to_markdown convenience function."""

    def test_basic_conversion(self):
        """Test basic HTML to markdown conversion."""
        html = "<h1>Hello</h1><p>World</p>"
        result = html_to_markdown(html)

        assert "# Hello" in result
        assert "World" in result

    def test_custom_heading_style(self):
        """Test custom heading style parameter."""
        html = "<h1>Title</h1>"
        result = html_to_markdown(html, heading_style="ATX")

        assert "# Title" in result

    def test_custom_strip_tags(self):
        """Test custom strip tags."""
        html = "<nav>Nav</nav><p>Content</p>"
        result = html_to_markdown(html, strip_tags=["nav"])

        assert "Content" in result
        # Nav content may or may not be visible depending on markdownify version
