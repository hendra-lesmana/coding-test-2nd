# Source Deduplication Feature

## Overview

The RAG-based Financial Q&A System now includes intelligent source deduplication to ensure that only unique, relevant source results are shown to users. This eliminates redundancy and improves the quality of responses by filtering out duplicate or highly similar content chunks.

## Features

### 1. Content Similarity Detection
- Uses `difflib.SequenceMatcher` to calculate similarity between content chunks
- Configurable similarity threshold (default: 0.75)
- Filters out content that is too similar to already selected sources

### 2. Page-based Source Limiting
- Limits the number of sources shown per page (default: 2 per page)
- Ensures diverse information from different parts of the document
- Prevents overwhelming users with multiple chunks from the same page

### 3. Two-level Deduplication
- **Retrieval Level**: Basic deduplication during vector search
- **Response Level**: Advanced content similarity analysis before presenting sources

## Configuration

### Environment Variables (.env)

```env
# Source Deduplication Configuration
ENABLE_SOURCE_DEDUPLICATION=True
CONTENT_SIMILARITY_THRESHOLD=0.75
MAX_SOURCES_PER_PAGE=2
```

### Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ENABLE_SOURCE_DEDUPLICATION` | `True` | Enable/disable source deduplication |
| `CONTENT_SIMILARITY_THRESHOLD` | `0.75` | Similarity threshold (0.0-1.0) for content deduplication |
| `MAX_SOURCES_PER_PAGE` | `2` | Maximum number of sources to show per page |

## How It Works

### 1. Document Retrieval
```python
# Vector store retrieves more documents initially
search_k = k * 2 if settings.enable_source_deduplication else k
results = self.vector_store.similarity_search_with_score(query, k=search_k)
```

### 2. Basic Deduplication at Retrieval
- Filters documents by page limits during retrieval
- Reduces processing overhead for similarity analysis

### 3. Advanced Content Similarity Analysis
```python
def _calculate_content_similarity(self, content1: str, content2: str) -> float:
    # Normalize content
    content1_norm = ' '.join(content1.lower().split())
    content2_norm = ' '.join(content2.lower().split())
    
    # Calculate similarity using SequenceMatcher
    similarity = SequenceMatcher(None, content1_norm, content2_norm).ratio()
    return similarity
```

### 4. Source Selection Process
1. **Page Limit Check**: Ensure max sources per page not exceeded
2. **Content Similarity Check**: Compare with already selected sources
3. **Threshold Filtering**: Only include sources below similarity threshold
4. **Quality Ranking**: Maintain sources with highest relevance scores

## Example Results

### Before Deduplication (5 sources)
```
Source 1: Page 1, Score: 0.95
  Content: The company's total revenue for 2024 was $1.2 billion, representing a 15% increase...

Source 2: Page 1, Score: 0.93
  Content: Total revenue for 2024 reached $1.2 billion, which is a 15% growth compared to 2023...

Source 3: Page 1, Score: 0.90
  Content: Operating expenses increased by 8% to $800 million in 2024...

Source 4: Page 2, Score: 0.88
  Content: Cash flow from operations was $400 million in 2024...

Source 5: Page 1, Score: 0.85
  Content: The net profit margin improved to 12% in 2024...
```

### After Deduplication (3 sources)
```
Source 1: Page 1, Score: 0.95
  Content: The company's total revenue for 2024 was $1.2 billion, representing a 15% increase...

Source 2: Page 1, Score: 0.90
  Content: Operating expenses increased by 8% to $800 million in 2024...

Source 3: Page 2, Score: 0.88
  Content: Cash flow from operations was $400 million in 2024...
```

**Filtered out:**
- Source 2 (similar to Source 1, similarity: 0.771 > 0.75)
- Source 5 (exceeded max sources per page limit)

## Frontend Integration

The frontend now displays the number of unique sources:

```tsx
<div className="flex items-center justify-between mb-1">
  <p className="text-xs font-medium text-gray-300">Sources:</p>
  <span className="text-xs text-gray-500">
    {message.sources.length} unique
  </span>
</div>
```

## Benefits

1. **Improved User Experience**: No redundant information
2. **Better Source Quality**: Only the most relevant and diverse sources
3. **Reduced Cognitive Load**: Easier to process fewer, higher-quality sources
4. **Configurable**: Can be adjusted based on use case requirements
5. **Performance**: Reduces unnecessary processing of duplicate content

## Testing

Run the deduplication test:

```bash
cd backend
python test_deduplication.py
```

This will demonstrate:
- Content similarity calculation
- Source filtering based on similarity threshold
- Page-based source limiting
- Before/after comparison

## Tuning Recommendations

### Content Similarity Threshold
- **0.9-1.0**: Very strict, only near-identical content filtered
- **0.7-0.8**: Balanced, filters similar content while preserving variety
- **0.5-0.6**: Aggressive, may filter content that's only moderately similar

### Max Sources Per Page
- **1**: Very restrictive, one source per page
- **2-3**: Balanced, allows some variety per page
- **4+**: Permissive, may allow too many sources from same page

## Monitoring

The system logs deduplication activity:

```
INFO:services.rag_pipeline:Deduplicated sources: 5 -> 3
DEBUG:services.rag_pipeline:Skipping duplicate source (similarity: 0.771)
DEBUG:services.rag_pipeline:Skipping source from page 1 - max sources per page reached
```

Monitor these logs to understand deduplication effectiveness and adjust thresholds as needed.
