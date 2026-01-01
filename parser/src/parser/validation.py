"""Validation utilities for references and metadata."""

import re
from dataclasses import dataclass
from urllib.parse import urlparse

from .parser import ParsedReference, ReferenceType


@dataclass
class ValidationError:
    """A validation error for a reference."""
    field: str
    message: str
    severity: str = "error"  # "error", "warning", "info"


@dataclass
class ValidationResult:
    """Result of validating a reference."""
    valid: bool
    errors: list[ValidationError]
    warnings: list[ValidationError]

    def __bool__(self) -> bool:
        return self.valid


def validate_reference(ref: ParsedReference) -> ValidationResult:
    """Validate a parsed reference.

    Args:
        ref: Reference to validate

    Returns:
        ValidationResult with errors and warnings
    """
    errors = []
    warnings = []

    # Validate year
    if ref.year:
        try:
            year_int = int(ref.year)
            if not (1900 <= year_int <= 2099):
                errors.append(ValidationError(
                    field="year",
                    message=f"Year {ref.year} is outside valid range (1900-2099)",
                    severity="error"
                ))
            elif year_int > 2030:
                warnings.append(ValidationError(
                    field="year",
                    message=f"Year {ref.year} is in the future",
                    severity="warning"
                ))
        except ValueError:
            errors.append(ValidationError(
                field="year",
                message=f"Year '{ref.year}' is not a valid integer",
                severity="error"
            ))

    # Validate DOI format
    if ref.type == ReferenceType.DOI:
        if not validate_doi(ref.value):
            errors.append(ValidationError(
                field="value",
                message=f"Invalid DOI format: {ref.value}",
                severity="error"
            ))

    # Validate arXiv ID format
    if ref.type == ReferenceType.ARXIV:
        if not validate_arxiv_id(ref.value):
            errors.append(ValidationError(
                field="value",
                message=f"Invalid arXiv ID format: {ref.value}",
                severity="error"
            ))

    # Validate URL
    if ref.url:
        if not validate_url(ref.url):
            errors.append(ValidationError(
                field="url",
                message=f"Invalid or malformed URL: {ref.url}",
                severity="error"
            ))

    # Validate GitHub repo format
    if ref.type == ReferenceType.GITHUB:
        if not validate_github_repo(ref.value):
            errors.append(ValidationError(
                field="value",
                message=f"Invalid GitHub repository format: {ref.value}",
                severity="error"
            ))

    # Check for missing metadata
    if ref.type == ReferenceType.PAPER:
        if not ref.title:
            warnings.append(ValidationError(
                field="title",
                message="Paper reference missing title",
                severity="warning"
            ))
        if not ref.authors:
            warnings.append(ValidationError(
                field="authors",
                message="Paper reference missing authors",
                severity="info"
            ))

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def validate_doi(doi: str) -> bool:
    """Validate DOI format.

    Args:
        doi: DOI string

    Returns:
        True if valid DOI format
    """
    # DOI must start with 10. followed by registrant code (4+ digits)
    # then slash and suffix
    pattern = r'^10\.\d{4,}/[^\s]+$'
    return bool(re.match(pattern, doi))


def classify_doi(doi: str) -> dict:
    """Classify a DOI to detect potential issues.
    
    Args:
        doi: DOI string
        
    Returns:
        Dict with classification info:
        - type: 'paper', 'book_chapter', 'review', 'dataset', 'unknown'
        - publisher: Publisher name if identified
        - is_paywalled: True if likely paywalled
        - warning: Warning message if any
    """
    result = {
        "type": "paper",
        "publisher": None,
        "is_paywalled": False,
        "warning": None
    }
    
    doi_lower = doi.lower()
    
    # Detect peer review DOIs (ScienceOpen reviews)
    # Pattern: 10.14293/s2199-1006.1.sor-...
    if "10.14293/" in doi_lower and "sor-" in doi_lower:
        result["type"] = "review"
        result["publisher"] = "ScienceOpen"
        result["warning"] = "This is a peer review DOI, not the actual paper. Look for the original paper DOI."
        return result
    
    # Faculty Opinions / F1000 recommendations: 10.3410/f.xxx
    if doi_lower.startswith("10.3410/f."):
        result["type"] = "review"
        result["publisher"] = "Faculty Opinions / F1000"
        result["warning"] = "This is a Faculty Opinions recommendation DOI, not the actual paper. Look for the original paper DOI."
        return result
    
    # Detect book chapter DOIs
    # Springer books: 10.1007/978-...
    if doi_lower.startswith("10.1007/978-"):
        result["type"] = "book_chapter"
        result["publisher"] = "Springer"
        result["is_paywalled"] = True
        result["warning"] = "This is a Springer book chapter DOI (likely paywalled). The original paper may have a different DOI or arXiv ID."
        return result
    
    # Elsevier books: 10.1016/b978-...
    if doi_lower.startswith("10.1016/b978-"):
        result["type"] = "book_chapter"
        result["publisher"] = "Elsevier"
        result["is_paywalled"] = True
        result["warning"] = "This is an Elsevier book chapter DOI (likely paywalled). The original paper may have a different DOI or arXiv ID."
        return result
    
    # Taylor & Francis / CRC Press books: 10.1201/9781... (978 is ISBN prefix)
    if doi_lower.startswith("10.1201/9781") or doi_lower.startswith("10.1201/978"):
        result["type"] = "book_chapter"
        result["publisher"] = "Taylor & Francis / CRC Press"
        result["is_paywalled"] = True
        result["warning"] = "This is a Taylor & Francis book chapter DOI (likely paywalled). The original paper may have a different DOI or arXiv ID."
        return result
    
    # Wiley books: 10.1002/978... (ISBN-based)
    if doi_lower.startswith("10.1002/978"):
        result["type"] = "book_chapter"
        result["publisher"] = "Wiley"
        result["is_paywalled"] = True
        result["warning"] = "This is a Wiley book chapter DOI (likely paywalled). The original paper may have a different DOI or arXiv ID."
        return result
    
    # Cambridge University Press books: 10.1017/978...
    if doi_lower.startswith("10.1017/978") or doi_lower.startswith("10.1017/cbo978"):
        result["type"] = "book_chapter"
        result["publisher"] = "Cambridge University Press"
        result["is_paywalled"] = True
        result["warning"] = "This is a Cambridge book chapter DOI (likely paywalled). The original paper may have a different DOI or arXiv ID."
        return result
    
    # Oxford University Press books: 10.1093/...978... or 10.1093/oso/978...
    if "10.1093/" in doi_lower and "978" in doi_lower:
        result["type"] = "book_chapter"
        result["publisher"] = "Oxford University Press"
        result["is_paywalled"] = True
        result["warning"] = "This is an Oxford book chapter DOI (likely paywalled). The original paper may have a different DOI or arXiv ID."
        return result
    
    # Detect common paywalled publishers
    paywalled_prefixes = {
        "10.1007/": "Springer",
        "10.1016/": "Elsevier",
        "10.1109/": "IEEE",
        "10.1145/": "ACM",
        "10.1002/": "Wiley",
    }
    
    for prefix, publisher in paywalled_prefixes.items():
        if doi_lower.startswith(prefix):
            result["publisher"] = publisher
            # These may have open access versions
            result["is_paywalled"] = True  # Assume paywalled, retriever will check for OA
            break
    
    # Detect dataset DOIs (Zenodo, Figshare, etc.)
    if "10.5281/zenodo" in doi_lower or "10.6084/" in doi_lower:
        result["type"] = "dataset"
        result["warning"] = "This appears to be a dataset DOI, not a paper."
    
    return result


def is_problematic_doi(doi: str) -> tuple[bool, str | None]:
    """Check if a DOI is problematic and should be skipped or flagged.
    
    Args:
        doi: DOI string
        
    Returns:
        Tuple of (is_problematic, reason)
    """
    classification = classify_doi(doi)
    
    if classification["type"] == "review":
        return True, classification["warning"]
    
    if classification["type"] == "book_chapter":
        return True, classification["warning"]
    
    if classification["type"] == "dataset":
        return True, classification["warning"]
    
    return False, None


def validate_arxiv_id(arxiv_id: str) -> bool:
    """Validate arXiv ID format.

    Args:
        arxiv_id: arXiv ID string

    Returns:
        True if valid arXiv ID format
    """
    # New format: YYMM.NNNNN or YYMM.NNNNNvN
    # Old format: archive/YYMMNNN
    new_pattern = r'^\d{4}\.\d{4,5}(v\d+)?$'
    old_pattern = r'^[a-z-]+/\d{7}$'
    return bool(re.match(new_pattern, arxiv_id) or re.match(old_pattern, arxiv_id))


def validate_url(url: str) -> bool:
    """Validate URL format and accessibility.

    Args:
        url: URL string

    Returns:
        True if URL appears valid
    """
    try:
        result = urlparse(url)
        # Must have scheme and netloc at minimum
        if not all([result.scheme, result.netloc]):
            return False
        # Scheme should be http or https
        if result.scheme not in ['http', 'https', 'ftp']:
            return False
        # Check for malformed URLs (missing closing parentheses, etc.)
        # Count parentheses
        open_parens = url.count('(')
        close_parens = url.count(')')
        if open_parens != close_parens:
            return False
        return True
    except Exception:
        return False


def validate_github_repo(repo: str) -> bool:
    """Validate GitHub repository format.

    Args:
        repo: Repository string (owner/repo format)

    Returns:
        True if valid format
    """
    # Must be owner/repo format
    if '/' not in repo:
        return False

    parts = repo.split('/')
    if len(parts) != 2:
        return False

    owner, name = parts
    # Basic validation: alphanumeric, hyphens, underscores
    # Owner and repo name must not be empty
    if not owner or not name:
        return False

    # Check for valid characters
    valid_chars = re.compile(r'^[a-zA-Z0-9_.-]+$')
    if not valid_chars.match(owner) or not valid_chars.match(name):
        return False

    return True


def validate_references(refs: list[ParsedReference], fix: bool = False) -> tuple[list[ParsedReference], list[ValidationResult]]:
    """Validate a list of references.

    Args:
        refs: List of references to validate
        fix: If True, attempt to fix common issues

    Returns:
        Tuple of (validated_refs, validation_results)
    """
    results = []
    validated_refs = []

    for ref in refs:
        result = validate_reference(ref)
        results.append(result)

        if result.valid:
            validated_refs.append(ref)
        elif fix:
            # Attempt to fix common issues
            fixed_ref = _fix_reference(ref, result)
            if fixed_ref:
                # Re-validate
                new_result = validate_reference(fixed_ref)
                if new_result.valid:
                    validated_refs.append(fixed_ref)
                    results[-1] = new_result

    return validated_refs, results


def _fix_reference(ref: ParsedReference, validation_result: ValidationResult) -> ParsedReference | None:
    """Attempt to fix common validation issues.

    Args:
        ref: Reference with validation issues
        validation_result: Validation result

    Returns:
        Fixed reference or None if cannot fix
    """
    from copy import deepcopy
    fixed = deepcopy(ref)

    for error in validation_result.errors:
        if error.field == "url" and error.message.startswith("Invalid or malformed URL"):
            # Try to fix missing closing parenthesis
            if fixed.url and '(' in fixed.url and fixed.url.count('(') > fixed.url.count(')'):
                fixed.url = fixed.url + ')'

    return fixed


# Known confusing terms that may cause false positive matches
CONFUSING_TERMS = {
    # AI model names that match real words/animals
    "llama": {
        "ai_context": ["language model", "meta", "ai", "llm", "foundation model", "transformer", "training"],
        "false_context": ["camelid", "animal", "herd", "veterinary", "mammal", "alpaca", "farm"],
        "ai_title_patterns": [r"llama\s*[23]?", r"llama\s*:\s*open"],
    },
    "falcon": {
        "ai_context": ["language model", "tii", "ai", "llm", "foundation model"],
        "false_context": ["bird", "raptor", "wildlife", "ornithology"],
    },
    "bert": {
        "ai_context": ["transformer", "nlp", "bidirectional", "pre-training", "language model"],
        "false_context": ["sesame street", "puppet", "name"],
        "ai_title_patterns": [r"bert\s*:", r"bert\s+pre-training"],
    },
}


def detect_title_context_mismatch(expected_title: str, actual_title: str, actual_abstract: str | None = None) -> tuple[bool, str | None]:
    """Detect if a retrieved paper title suggests a context mismatch.
    
    This catches cases like searching for "LLaMA" (AI model) and getting
    "Camelid Herd Health" (about actual llamas).
    
    Args:
        expected_title: The title we're looking for
        actual_title: The title of the paper that was found
        actual_abstract: Optional abstract text for additional context
        
    Returns:
        Tuple of (is_mismatch, reason)
    """
    expected_lower = expected_title.lower()
    actual_lower = actual_title.lower()
    abstract_lower = (actual_abstract or "").lower()
    
    combined_actual = f"{actual_lower} {abstract_lower}"
    
    for term, contexts in CONFUSING_TERMS.items():
        # Check if the confusing term appears in expected title
        if term not in expected_lower:
            continue
            
        # Check if actual paper has false positive indicators
        false_indicators = contexts.get("false_context", [])
        ai_indicators = contexts.get("ai_context", [])
        
        false_score = sum(1 for ind in false_indicators if ind in combined_actual)
        ai_score = sum(1 for ind in ai_indicators if ind in combined_actual)
        
        # If actual paper has more false indicators than AI indicators, flag it
        if false_score > ai_score and false_score >= 2:
            return True, f"Title mismatch: '{actual_title}' appears to be about {term} (the animal/entity), not {term.upper()} (the AI model). Found {false_score} non-AI indicators: {[ind for ind in false_indicators if ind in combined_actual]}"
        
        # Check if expected has AI patterns but actual doesn't match
        ai_patterns = contexts.get("ai_title_patterns", [])
        expected_is_ai = any(re.search(pat, expected_lower, re.IGNORECASE) for pat in ai_patterns)
        actual_is_ai = any(re.search(pat, actual_lower, re.IGNORECASE) for pat in ai_patterns)
        
        if expected_is_ai and not actual_is_ai and false_score > 0:
            return True, f"Title mismatch: Expected AI paper matching '{expected_title}', but found '{actual_title}' which appears unrelated."
    
    return False, None


def validate_paper_match(expected_title: str, actual_doi: str, actual_metadata: dict | None = None) -> tuple[bool, str | None]:
    """Validate that a DOI actually matches the expected paper.
    
    Args:
        expected_title: The title we're looking for
        actual_doi: The DOI that was found
        actual_metadata: Optional metadata from the DOI resolver
        
    Returns:
        Tuple of (is_valid_match, warning_message)
    """
    # First check DOI classification
    is_problematic, doi_warning = is_problematic_doi(actual_doi)
    if is_problematic:
        return False, doi_warning
    
    # If we have metadata, check title match
    if actual_metadata:
        actual_title = actual_metadata.get("title", "")
        actual_abstract = actual_metadata.get("abstract", "")
        
        is_mismatch, mismatch_reason = detect_title_context_mismatch(
            expected_title, actual_title, actual_abstract
        )
        if is_mismatch:
            return False, mismatch_reason
    
    return True, None

