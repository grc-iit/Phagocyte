"""Parser for extracting references from research documents.

Takes in a research document and generates a list of PDFs, websites,
citations, git repos, YouTube videos, podcasts, books, etc. referenced in it.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ReferenceType(Enum):
    """Types of references that can be extracted."""
    GITHUB = "github"
    ARXIV = "arxiv"
    DOI = "doi"
    PAPER = "paper"
    BLOG = "blog"  # Blog posts, articles (Towards Data Science, Medium, etc.)
    PDF = "pdf"
    YOUTUBE = "youtube"
    PODCAST = "podcast"
    BOOK = "book"
    WEBSITE = "website"


@dataclass
class ParsedReference:
    """A reference extracted from research output."""
    type: ReferenceType
    value: str
    title: str = ""
    authors: str = ""
    year: str = ""
    url: str | None = None
    context: str = ""
    metadata: dict = field(default_factory=dict)


class ResearchParser:
    """Parser for extracting references from research documents.

    Takes in a research document and generates a categorized list of:
    - PDFs
    - Websites
    - Citations (papers)
    - Git repositories
    - YouTube videos
    - Podcasts
    - Books

    Example:
        ```python
        parser = ResearchParser()
        refs = parser.parse_file("research_report.md")

        # Get summary
        summary = parser.get_summary(refs)
        print(summary)

        # Get by category
        github_repos = [r for r in refs if r.type == ReferenceType.GITHUB]
        ```
    """

    def __init__(self):
        """Initialize the parser."""
        pass

    def parse(self, text: str) -> list[ParsedReference]:
        """Parse text and extract all references.

        Args:
            text: Text content to parse

        Returns:
            List of parsed references
        """
        references = []

        # Extract GitHub repos
        references.extend(self._extract_github(text))

        # Extract arXiv papers
        references.extend(self._extract_arxiv(text))

        # Extract DOIs
        references.extend(self._extract_doi(text))

        # Extract paper citations (Author et al., Year)
        references.extend(self._extract_papers(text))

        # Extract PDFs
        references.extend(self._extract_pdfs(text))

        # Extract YouTube
        references.extend(self._extract_youtube(text))

        # Extract podcasts
        references.extend(self._extract_podcasts(text))

        # Extract books
        references.extend(self._extract_books(text))

        # Extract general websites
        references.extend(self._extract_websites(text))

        # Deduplicate
        references = self._deduplicate(references)

        return references

    def parse_file(self, file_path: Path) -> list[ParsedReference]:
        """Parse a file and extract references.

        Args:
            file_path: Path to file

        Returns:
            List of parsed references
        """
        file_path = Path(file_path)

        if file_path.suffix == ".json":
            import json
            with open(file_path) as f:
                data = json.load(f)
            if isinstance(data, dict):
                text = data.get("report", data.get("content", str(data)))
                if text is None:
                    text = str(data)
            else:
                text = str(data)
        else:
            text = file_path.read_text()

        return self.parse(str(text))

    def _extract_github(self, text: str) -> list[ParsedReference]:
        """Extract GitHub repositories."""
        refs = []
        seen = set()

        patterns = [
            # **Repository:** `owner/repo`
            r'\*\*Repository:\*\*\s*`([a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)`',
            # `owner/repo` format
            r'`([a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)`',
            # GitHub URLs
            r'github\.com/([a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                repo = match.group(1).rstrip('/')
                # Clean up repo name
                repo = repo.split('/tree/')[0].split('/blob/')[0]

                if repo not in seen and '/' in repo:
                    seen.add(repo)
                    refs.append(ParsedReference(
                        type=ReferenceType.GITHUB,
                        value=repo,
                        title=repo.split('/')[-1],
                        url=f"https://github.com/{repo}",
                        context=self._get_context(text, match),
                    ))

        return refs

    def _extract_arxiv(self, text: str) -> list[ParsedReference]:
        """Extract arXiv papers."""
        refs = []
        seen = set()

        patterns = [
            # arXiv:2301.00001 or arXiv: 2301.00001v2
            r'arXiv[:\s]+(\d{4}\.\d{4,5})(?:v\d+)?',
            # arxiv.org/abs/2301.00001
            r'arxiv\.org/abs/(\d{4}\.\d{4,5})(?:v\d+)?',
            # arxiv.org/pdf/2301.00001.pdf or arxiv.org/pdf/2301.00001v2.pdf
            r'arxiv\.org/pdf/(\d{4}\.\d{4,5})(?:v\d+)?\.pdf',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                arxiv_id = match.group(1)
                # Strip version suffix for deduplication (we keep base ID)
                base_id = arxiv_id.split('v')[0] if 'v' in arxiv_id else arxiv_id
                if base_id not in seen:
                    seen.add(base_id)
                    refs.append(ParsedReference(
                        type=ReferenceType.ARXIV,
                        value=base_id,
                        url=f"https://arxiv.org/abs/{base_id}",
                        context=self._get_context(text, match),
                    ))

        return refs

    def _extract_doi(self, text: str) -> list[ParsedReference]:
        """Extract DOIs, with classification for problematic types."""
        from .validation import classify_doi
        
        refs = []
        seen = set()

        patterns = [
            # DOI pattern - exclude backticks, brackets, parens, and common punctuation
            r'(?:doi[:\s]+)?(10\.\d{4,}/[^\s\]\)\[\(,`\'"]+)',
            r'doi\.org/(10\.\d{4,}/[^\s\]\)\[\(,`\'"]+)',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Strip trailing punctuation including backticks
                doi = match.group(1).rstrip('.,;:`\'"')
                # Normalize the DOI
                doi = doi.strip()
                if doi not in seen and doi:
                    seen.add(doi)
                    
                    # Classify the DOI to detect potential issues
                    classification = classify_doi(doi)
                    metadata = {}
                    if classification.get("warning"):
                        metadata["doi_warning"] = classification["warning"]
                        metadata["doi_type"] = classification["type"]
                        metadata["publisher"] = classification.get("publisher")
                        metadata["is_paywalled"] = classification.get("is_paywalled", False)
                    
                    refs.append(ParsedReference(
                        type=ReferenceType.DOI,
                        value=doi,
                        url=f"https://doi.org/{doi}",
                        context=self._get_context(text, match),
                        metadata=metadata,
                    ))

        return refs

    def _extract_papers(self, text: str) -> list[ParsedReference]:
        """Extract paper citations and blog posts."""
        refs = []
        seen = set()
        
        # Keywords that indicate NOT a paper (videos only)
        non_paper_indicators = [
            'youtube', 'video',
        ]
        
        # Keywords that indicate a documentation/website ref, not an academic paper
        doc_indicators = [
            'user guide', 'documentation', 'readthedocs',
            'api reference', 'getting started',
        ]
        
        # Keywords that indicate a BLOG POST (not academic paper)
        # These are publications without DOIs, typically on blogging platforms
        blog_source_indicators = [
            'towards data science', 'towardsdatascience', 'medium',
            'the hdf group', 'hdf group', 'romio blog', 'blog',
            'dev.to', 'substack', 'hashnode', 'freecodecamp',
            'analytics vidhya', 'kdnuggets', 'datacamp',
        ]

        # **Paper:** *Title*
        paper_pattern = r'\*\*Paper:\*\*\s*\*([^*]+)\*'
        for match in re.finditer(paper_pattern, text):
            title = match.group(1).strip()
            if title.lower() not in seen:
                seen.add(title.lower())
                refs.append(ParsedReference(
                    type=ReferenceType.PAPER,
                    value=title,
                    title=title,
                    context=self._get_context(text, match),
                ))

        # **Authors:** Author et al. **Year:** 2020

        # Title (Author et al., Year)
        cite_pattern = r'"([^"]{15,200})"\s*\(([A-Z][a-z]+(?:\s+et\s+al\.?)?),?\s*(\d{4})\)'
        for match in re.finditer(cite_pattern, text):
            title = match.group(1).strip()
            authors = match.group(2)
            year = match.group(3)
            context = self._get_context(text, match)
            
            # Skip if context indicates this is a video
            context_lower = context.lower()
            if any(ind in context_lower for ind in non_paper_indicators):
                continue
                
            if title.lower() not in seen:
                seen.add(title.lower())
                refs.append(ParsedReference(
                    type=ReferenceType.PAPER,
                    value=title,
                    title=title,
                    authors=authors,
                    year=year,
                    context=match.group(0),
                ))

        # [N] "Paper Title" (Author et al.). *Venue*, Year. [N]
        # Updated: Support venue in italics (*Venue*) and year at end
        ref_list_pattern = r'\[(\d+)\]\s*"([^"]{10,200})"\s*\(([^)]+)\)\.?\s*(?:\*([^*]+)\*)?[,.]?\s*(\d{4})?\.'
        for match in re.finditer(ref_list_pattern, text):
            title = match.group(2).strip()
            authors = match.group(3).strip()
            venue = match.group(4).strip() if match.group(4) else ""
            year = match.group(5) if match.group(5) else ""

            # Also try to extract year from end of line if not captured
            if not year:
                context = self._get_context(text, match)
                year_match = re.search(r'(\d{4})\.\s*\[\d+\]\s*$', context)
                if year_match:
                    year = year_match.group(1)

            # Validate year - must be between 1900-2099
            if year:
                try:
                    year_int = int(year)
                    if not (1900 <= year_int <= 2099):
                        year = ""
                except ValueError:
                    year = ""

            context = self._get_context(text, match)
            context_lower = context.lower()

            # Skip if this is a video reference
            if any(ind in context_lower for ind in non_paper_indicators):
                continue

            # Check if this is an academic paper (has "et al" in authors)
            is_academic = 'et al' in authors.lower()
            
            # Only apply doc filter to non-academic refs (no "et al")
            # Academic papers with "schema", "guide" etc in title should be kept
            if not is_academic:
                title_lower = title.lower()
                if any(ind in title_lower for ind in doc_indicators):
                    continue

            # Check if this is a blog post (non-academic with blog source in author OR venue)
            authors_lower = authors.lower()
            venue_lower = venue.lower() if venue else ""
            is_blog = not is_academic and (
                any(ind in authors_lower for ind in blog_source_indicators) or
                any(ind in venue_lower for ind in blog_source_indicators)
            )

            if title.lower() not in seen:
                seen.add(title.lower())
                refs.append(ParsedReference(
                    type=ReferenceType.BLOG if is_blog else ReferenceType.PAPER,
                    value=title,
                    title=title,
                    authors=authors,
                    year=year,
                    context=self._get_context(text, match),
                ))

        # [N] "Title" (Source). Year. [N]  - for blog posts without et al.
        # e.g., [5] "Which data format..." (Towards Data Science). 2023.
        blog_pattern = r'\[(\d+)\]\s*"([^"]{10,200})"\s*\(([^)]+)\)\.?\s*(\d{4})\.'
        for match in re.finditer(blog_pattern, text):
            title = match.group(2).strip()
            source = match.group(3).strip()
            year = match.group(4)
            
            # Skip if already captured by ref_list_pattern
            if title.lower() in seen:
                continue
            
            # Skip videos
            context = self._get_context(text, match)
            context_lower = context.lower()
            if any(ind in context_lower for ind in non_paper_indicators):
                continue
            
            # Skip documentation entries
            title_lower = title.lower()
            if any(ind in title_lower for ind in doc_indicators):
                continue
            
            # Determine if this is a blog post or paper based on source
            source_lower = source.lower()
            is_blog = any(ind in source_lower for ind in blog_source_indicators)
            
            seen.add(title.lower())
            refs.append(ParsedReference(
                type=ReferenceType.BLOG if is_blog else ReferenceType.PAPER,
                value=title,
                title=title,
                authors=source,  # Source as author (e.g., "Towards Data Science")
                year=year,
                context=self._get_context(text, match),
            ))

        # Conference/Journal citation: "Title" (Author et al.). Venue, Year. DOI/URL
        # Updated pattern to avoid matching years from arXiv IDs (match after whitespace/comma)
        venue_pattern = r'"([^"]{15,200})"\s*\(([^)]+)\)\.\s*(?:arXiv|NeurIPS|ICLR|ICML|ACL|NAACL|EMNLP|CVPR|ICCV|ECCV|Nature|Science)[^,\n]*,\s*(\d{4})\b'
        for match in re.finditer(venue_pattern, text):
            title = match.group(1).strip()
            authors = match.group(2).strip()
            year = match.group(3)

            # Validate year - must be between 1900-2099
            if year:
                try:
                    year_int = int(year)
                    if not (1900 <= year_int <= 2099):
                        # Invalid year (likely from arXiv ID), try to find real year
                        context = self._get_context(text, match)
                        year_match = re.search(r'\b(19|20)\d{2}\b', context)
                        if year_match:
                            potential_year = int(year_match.group(0))
                            if 1900 <= potential_year <= 2099:
                                year = year_match.group(0)
                            else:
                                year = ""
                        else:
                            year = ""
                except ValueError:
                    year = ""

            if title.lower() not in seen:
                seen.add(title.lower())
                refs.append(ParsedReference(
                    type=ReferenceType.PAPER,
                    value=title,
                    title=title,
                    authors=authors,
                    year=year,
                    context=self._get_context(text, match),
                ))

        return refs

    def _extract_pdfs(self, text: str) -> list[ParsedReference]:
        """Extract PDF links."""
        refs = []
        seen = set()

        pattern = r'(https?://[^\s\]\)]+\.pdf)'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            url = match.group(1)
            if url not in seen:
                seen.add(url)
                refs.append(ParsedReference(
                    type=ReferenceType.PDF,
                    value=url,
                    url=url,
                    context=self._get_context(text, match),
                ))

        return refs

    def _extract_youtube(self, text: str) -> list[ParsedReference]:
        """Extract YouTube videos."""
        refs = []
        seen = set()

        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                video_id = match.group(1)
                if video_id not in seen:
                    seen.add(video_id)
                    refs.append(ParsedReference(
                        type=ReferenceType.YOUTUBE,
                        value=video_id,
                        url=f"https://youtube.com/watch?v={video_id}",
                        context=self._get_context(text, match),
                    ))

        return refs

    def _extract_podcasts(self, text: str) -> list[ParsedReference]:
        """Extract podcast references."""
        refs = []
        seen = set()

        # Podcast mentions
        patterns = [
            r'(?:podcast|episode)[:\s]+["\']([^"\']+)["\']',
            r'(spotify\.com/(?:show|episode)/[^\s\]\)]+)',
            r'(podcasts\.apple\.com/[^\s\]\)]+)',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                value = match.group(1)
                if value.lower() not in seen:
                    seen.add(value.lower())
                    url = value if value.startswith('http') or '.' in value else None
                    refs.append(ParsedReference(
                        type=ReferenceType.PODCAST,
                        value=value,
                        url=f"https://{url}" if url and not url.startswith('http') else url,
                        context=self._get_context(text, match),
                    ))

        return refs

    def _extract_books(self, text: str) -> list[ParsedReference]:
        """Extract book references."""
        refs = []
        seen = set()

        # Known non-books to filter out (PEPs, manifestos, academic papers, etc.)
        non_books = {
            'the zen of python',
            'pep 8',
            'pep 20',
            'pep 484',
        }
        
        # Academic paper keywords - if title contains these, likely a paper not book
        paper_keywords = [
            'attention', 'transformer', 'neural', 'learning', 'deep',
            'bert', 'gpt', 'language model', 'recognition', 'detection',
            'classification', 'segmentation', 'pre-training', 'pretraining',
        ]

        # Book patterns
        patterns = [
            # "Book Title" by Author
            (r'"([^"]{10,100})"\s+by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'title_author'),
            # ISBN-13 with various prefixes (ISBN-13:, ISBN 13:, ISBN13:, ISBN:, ISBN )
            # Must be 13 digits starting with 978 or 979, followed by non-digit
            (r'ISBN(?:[- ]?13)?[:\s]*(97[89]\d{10})(?!\d)', 'isbn'),
            # ISBN-10 with various prefixes (ISBN-10:, ISBN 10:, ISBN10:, ISBN:, ISBN )
            # Must be exactly 10 digits/X, followed by non-digit
            (r'ISBN(?:[- ]?10)?[:\s]*(\d{9}[\dXx])(?!\d)', 'isbn'),
            # **Book:** Title
            (r'\*\*Book:\*\*\s*\*?([^*\n]+)\*?', 'title'),
        ]

        for pattern, pattern_type in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                if pattern_type == 'isbn':
                    isbn = match.group(1)
                    # Validate ISBN length - must be exactly 10 or 13 digits
                    if len(isbn) != 10 and len(isbn) != 13:
                        continue
                    value = f"ISBN: {isbn}"
                    title = ""
                    authors = ""
                else:
                    value = match.group(1).strip()
                    title = value
                    authors = match.group(2) if match.lastindex is not None and match.lastindex >= 2 else ""

                # Skip known non-books
                if value.lower() in non_books or title.lower() in non_books:
                    continue
                
                # Skip if title looks like an academic paper
                title_lower = title.lower() if title else value.lower()
                if any(kw in title_lower for kw in paper_keywords):
                    continue

                if value.lower() not in seen:
                    seen.add(value.lower())
                    refs.append(ParsedReference(
                        type=ReferenceType.BOOK,
                        value=value,
                        title=title,
                        authors=authors,
                        context=self._get_context(text, match),
                    ))

        return refs

    def _extract_websites(self, text: str) -> list[ParsedReference]:
        """Extract general website URLs."""
        refs = []
        seen = set()
        seen_url_bases = set()  # Track normalized URL bases to avoid partial matches

        # Skip patterns for other types (already extracted elsewhere)
        skip_patterns = [
            'github.com', 'arxiv.org', 'doi.org', 'youtube.com', 'youtu.be',
            'spotify.com', 'podcasts.apple.com', '.pdf',
            'vertexaisearch.cloud.google.com',  # Skip redirect URLs
        ]
        
        # Skip patterns for academic paper hosting sites (papers already extracted as PAPER type)
        academic_skip_patterns = [
            'papers.nips.cc', 'proceedings.neurips.cc', 'openreview.net',
            'aclweb.org', 'aclanthology.org', 'anthology.aclweb.org',
            'proceedings.mlr.press', 'jmlr.org', 'ijcai.org',
            'aaai.org/ojs', 'aaai.org/ocs', 'dl.acm.org',
            'ieeexplore.ieee.org', 'sciencedirect.com', 'springer.com/article',
            'nature.com/articles', 'pnas.org', 'plos.org',
            'frontiersin.org/articles', 'mdpi.com',
            'biorxiv.org', 'medrxiv.org',  # Preprint servers
            'semanticscholar.org/paper',  # Semantic Scholar paper pages
            'openaccess.thecvf.com',  # CVPR/ICCV papers
        ]
        
        def normalize_url(url: str) -> str:
            """Normalize URL for comparison - strip trailing punctuation and closing parens."""
            return url.rstrip('.,;:"\'[])(').rstrip(')')

        # Match URLs, handling parentheses in Wikipedia URLs properly
        # First try to match URLs with balanced parentheses (for Wikipedia)
        wiki_pattern = r'https?://[^\s\]>]+\([^)]+\)'
        for match in re.finditer(wiki_pattern, text):
            url = match.group(0).rstrip('.,;:"\'[]')
            
            # Skip if matches other types
            if any(skip in url.lower() for skip in skip_patterns):
                continue
            
            # Skip academic paper hosting sites
            if any(skip in url.lower() for skip in academic_skip_patterns):
                continue

            if url not in seen:
                seen.add(url)
                # Track the normalized URL base (with and without closing paren) to avoid partial matches
                normalized = normalize_url(url)
                seen_url_bases.add(normalized)
                # Also track version without trailing parenthesis content
                if '(' in url:
                    base_before_paren = url.split('(')[0]
                    seen_url_bases.add(base_before_paren)
                    # Track partial match (URL up to but not including closing paren)
                    paren_idx = url.rfind('(')
                    if paren_idx > 0:
                        seen_url_bases.add(url[:paren_idx] + url[paren_idx:].rstrip(')'))
                
                domain = re.search(r'https?://([^/]+)', url)
                title = domain.group(1) if domain else url
                refs.append(ParsedReference(
                    type=ReferenceType.WEBSITE,
                    value=url,
                    title=title,
                    url=url,
                    context=self._get_context(text, match),
                ))

        # Then match regular URLs
        pattern = r'https?://[^\s\]\)>]+'
        for match in re.finditer(pattern, text):
            url = match.group(0).rstrip('.,;:"\'[]()')

            # Skip if matches other types
            if any(skip in url.lower() for skip in skip_patterns):
                continue
            
            # Skip academic paper hosting sites
            if any(skip in url.lower() for skip in academic_skip_patterns):
                continue
            
            # Skip if this URL (or normalized version) was already seen
            # This handles Wikipedia URLs where we might match partial URL
            normalized = normalize_url(url)
            if normalized in seen_url_bases or url in seen_url_bases:
                continue

            if url not in seen:
                seen.add(url)
                seen_url_bases.add(normalized)
                # Extract domain as title
                domain = re.search(r'https?://([^/]+)', url)
                title = domain.group(1) if domain else url

                refs.append(ParsedReference(
                    type=ReferenceType.WEBSITE,
                    value=url,
                    title=title,
                    url=url,
                    context=self._get_context(text, match),
                ))

        return refs

    def _get_context(self, text: str, match) -> str:
        """Get surrounding context for a match."""
        start = max(0, match.start() - 50)
        end = min(len(text), match.end() + 50)
        return text[start:end].strip()

    def _deduplicate(self, refs: list[ParsedReference]) -> list[ParsedReference]:
        """Remove duplicate references.
        
        Handles both same-type duplicates (same type + value) and cross-type
        duplicates (e.g., paper title extracted as PAPER but also has URL as WEBSITE).
        """
        seen_by_type = set()  # (type, value) pairs
        seen_urls = set()  # Track all URLs to avoid duplicates across types
        unique = []

        for ref in refs:
            key = (ref.type, ref.value.lower())
            
            # Skip if exact same type+value already seen
            if key in seen_by_type:
                continue
            
            # Skip if URL already seen from another extraction
            if ref.url and ref.url.lower() in seen_urls:
                continue
            
            seen_by_type.add(key)
            if ref.url:
                seen_urls.add(ref.url.lower())
            unique.append(ref)

        return unique

    def group_by_type(self, refs: list[ParsedReference]) -> dict[ReferenceType, list[ParsedReference]]:
        """Group references by type."""
        grouped: dict[ReferenceType, list[ParsedReference]] = {}
        for ref in refs:
            if ref.type not in grouped:
                grouped[ref.type] = []
            grouped[ref.type].append(ref)
        return grouped

    def get_summary(self, refs: list[ParsedReference]) -> str:
        """Generate a summary of extracted references.

        Args:
            refs: List of references

        Returns:
            Formatted summary string
        """
        grouped = self.group_by_type(refs)

        lines = ["# Extracted References\n"]

        type_names = {
            ReferenceType.GITHUB: "GitHub Repositories",
            ReferenceType.ARXIV: "arXiv Papers",
            ReferenceType.DOI: "DOI Citations",
            ReferenceType.PAPER: "Paper Citations",
            ReferenceType.PDF: "PDF Documents",
            ReferenceType.YOUTUBE: "YouTube Videos",
            ReferenceType.PODCAST: "Podcasts",
            ReferenceType.BOOK: "Books",
            ReferenceType.WEBSITE: "Websites",
        }

        for ref_type in ReferenceType:
            if ref_type in grouped:
                type_refs = grouped[ref_type]
                lines.append(f"\n## {type_names.get(ref_type, ref_type.value)} ({len(type_refs)})\n")

                for ref in type_refs:
                    if ref.url:
                        lines.append(f"- [{ref.value}]({ref.url})")
                    else:
                        lines.append(f"- {ref.value}")

                    if ref.authors or ref.year:
                        extra = []
                        if ref.authors:
                            extra.append(ref.authors)
                        if ref.year:
                            extra.append(ref.year)
                        lines.append(f"  - {', '.join(extra)}")

        # Summary stats
        lines.append(f"\n---\n**Total: {len(refs)} references**")

        return "\n".join(lines)

    def save_summary(self, refs: list[ParsedReference], output_path: Path) -> Path:
        """Save summary to a file.

        Args:
            refs: List of references
            output_path: Output directory or file path

        Returns:
            Path to saved file
        """
        output_path = Path(output_path)

        if output_path.is_dir():
            output_path = output_path / "extracted_references.md"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.get_summary(refs))

        return output_path
