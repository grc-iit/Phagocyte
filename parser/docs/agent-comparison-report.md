# Agent vs Regular Parsing Comparison Report

**Date:** December 30, 2025  
**Test Document:** `research_report.md` (Transformer Architecture and Attention Mechanisms)

---

## Summary

| Parser | Total References | Execution |
|--------|------------------|-----------|
| **Regular (regex)** | 26 | ✅ Fast, no API needed |
| **Claude Agent** | 34 | ✅ Works (uses Claude Code CLI) |
| **Gemini Agent** | N/A | ⚠️ API quota exceeded |

---

## Detailed Comparison: Regular vs Claude Agent

### Reference Counts by Type

| Type | Regular | Claude Agent |
|------|---------|--------------|
| **paper** | 1 | 12 |
| **doi** | 4 | 4 |
| **arxiv** | 3 | 3 |
| **website** | 9 | 8 |
| **github** | 4 | 4 |
| **youtube** | 3 | 3 |
| **pdf** | 1 | 0 |
| **book** | 1 | 0 |
| **TOTAL** | **26** | **34** |

### Overlap Analysis

- **Common references:** 14
- **Only in Regular:** 12
- **Only in Claude Agent:** 20

### What Each Parser Found Uniquely

#### Only Found by Regular (regex-based) Parsing:

1. `[book]` Attention Is All You Need
2. `[paper]` An Image is Worth 16x16 Words
3. `[pdf]` https://openaccess.thecvf.com/content/ICCV2021/papers/Liu_Swin_Transformer...
4. `[website]` http://nlp.seas.harvard.edu/2018/04/03/attention.html
5. `[website]` https://aclanthology.org/N19-1423
6. `[website]` https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)
7. `[website]` https://huggingface.co/docs/transformers
8. `[website]` https://jalammar.github.io/illustrated-transformer/
9. `[website]` https://openreview.net/forum?id=YicbFdNTTy
10. `[website]` https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html
11. `[website]` https://pytorch.org/tutorials/beginner/transformer_tutorial.html
12. `[website]` https://towardsdatascience.com/transformers-from-nlp-to-computer-vision-4f237386610c/

#### Only Found by Claude Agent Parsing:

1. `[paper]` An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale
2. `[paper]` Attention Is All You Need
3. `[paper]` BART
4. `[paper]` CLIP (Contrastive Language-Image Pre-training)
5. `[paper]` DETR (Detection Transformer)
6. `[paper]` GPT-1
7. `[paper]` GPT-3
8. `[paper]` LSTM (Long Short-Term Memory)
9. `[paper]` NLLB (No Language Left Behind)
10. `[paper]` ResNet
11. `[paper]` RNN (Recurrent Neural Networks)
12. `[paper]` T5
13. `[paper]` ViT (Vision Transformer)
14. `[paper]` Swin Transformer
15. ... and more inline paper mentions

---

## Key Findings

### Strengths of Regular (Regex) Parsing:

1. **Fast execution** - No API calls needed
2. **Reliable URL detection** - Captures all explicit URLs
3. **PDF detection** - Extracts direct PDF links
4. **Book pattern detection** - Identifies book-style citations

### Weaknesses of Regular Parsing:

1. **Misses inline paper mentions** - Can't detect "GPT-3", "BERT", "ResNet" when mentioned without URLs
2. **No semantic understanding** - Only pattern matching

### Strengths of Claude Agent Parsing:

1. **Semantic understanding** - Recognizes paper names mentioned in text (BART, CLIP, DETR, etc.)
2. **Better paper extraction** - Finds 12 papers vs 1
3. **Context awareness** - Understands "the GPT series" refers to papers

### Weaknesses of Claude Agent Parsing:

1. **Slower execution** - Requires API call
2. **Missed some URLs** - Didn't capture all website URLs that regex found
3. **No PDF detection** - Missed the direct PDF link
4. **Inconsistent** - Results vary slightly between runs

---

## Issues to Fix

### 1. Regular Parser Issues:

| Issue | Description | Priority |
|-------|-------------|----------|
| Limited paper detection | Only detects papers with specific citation patterns | Medium |
| Book vs Paper confusion | "Attention Is All You Need" detected as book, not paper | Low |

### 2. Claude Agent Issues:

| Issue | Description | Priority |
|-------|-------------|----------|
| Missing PDF URLs | Agent doesn't extract direct PDF links | High |
| Missing some website URLs | Lost 4 website references that regex found | Medium |
| Empty results on some runs | First comparison run returned 0 refs | Low |

### 3. Gemini Agent Issues:

| Issue | Description | Priority |
|-------|-------------|----------|
| API quota limits | Free tier quota exceeded quickly | High |
| Need retry logic | Should handle 429 errors gracefully | High |

---

## Recommendations

### For Best Results:

1. **Use `--compare` mode** to run both parsers and combine results
2. **Regular parser** for: URLs, DOIs, arXiv IDs, GitHub repos, YouTube
3. **Agent parser** for: Inline paper mentions, semantic extraction

### Code Improvements Needed:

1. Add retry logic with exponential backoff for Gemini quota errors
2. Improve agent prompt to explicitly request PDF URLs
3. Consider merging results from both parsers automatically
4. Add `--merge` flag to combine regular + agent results

---

## CLI Usage Reference

```bash
# Regular parsing (fast, no API)
parser parse-refs document.md

# Claude agent (no API key needed - uses Claude Code CLI)
parser parse-refs document.md --agent claude

# Anthropic API (requires ANTHROPIC_API_KEY)
parser parse-refs document.md --agent anthropic

# Gemini via Google ADK (requires GOOGLE_API_KEY)
parser parse-refs document.md --agent gemini

# Google API directly (requires GOOGLE_API_KEY)
parser parse-refs document.md --agent google

# Compare regular vs agent
parser parse-refs document.md --agent claude --compare
```

---

## Test Output Locations

- `test_output/comparison_test2/regular/` - Regular parsing results
- `test_output/comparison_test2/agent/` - Claude agent results
- `test_output/comparison_test2/comparison_report.md` - Side-by-side comparison
