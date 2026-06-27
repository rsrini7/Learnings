## 1. Document Consolidation & Integration Prompts
Prompts focused on combining, merging, and creating comprehensive single documents from multiple sources.

### 1.1 Full Consolidation with Complete Coverage
> Give me Consolidated single Markdown document covering all shared documents. Don't miss any of the information. Take Time.. not just key points, should cover all aspects, verify then combine each section by comparing all the documents and merge it.

### 1.2 Whitepaper Creation for Technical Audiences
> Understand the given context, youtube videos if given Watch each video. Create very simple whitepaper for developer and architects, go deeper search, but reduce too many source code examples. Verify, compare and then provide all in one markdown document with illustration, examples. performance references and so on in simple clear and concise and simplified English markdown file. if any diagrams required, generate mermaid syntax only. When generating mermaid diagrams if any make sure to add double quotes the contents inside square bracket (but don't escape the double quotes if already exist).

### 1.3 Comprehensive Document Creation with Visuals
> Review, Search and give me single well markdown document covering all shared documents. Don't miss any of the information. You should produce single content covering all. Explain well but simple English. Use mermaid diagrams, do compare, illustration, examples. performance and so on. But reduce too many source code examples.

### 1.4 Enhanced Documentation with Missing Details
> Review, Search and give me single well markdown document covering all missing relavent details. Don't miss any of the information from existing md file. Explain well but simple English. Use mermaid diagrams, do compare, illustration, examples and so on.

### 1.5 Merging and Updating Existing Documents
> Review, Search , merge and give me single well markdown document covering all missing relevant details. Make sure to keep information from existing md file which are not requires any changes.

---

## 2. Document Review & Validation Prompts
Prompts focused on checking for errors, verifying accuracy, and improving existing documents.

### 2.1 Error Detection and Validation
> Do Research, REVIEW end to end and provide any possible errors , wrong interpretations, mis representation. Give me clear concise reviews.

### 2.2 Complete Guide Rewrite and Verification
> Rewrite the entire Complete Guide and give me single markdown and if needed modify mermaid diagrams, source code , but keep as much information as possible by reviewing with realtime basis , do not hullusinate if the information is not able to verify.

---

## 3. Research & Analysis Prompts
Prompts designed for analyzing research papers and technical content.

### 3.1 AI Abstract Summarization
> Do AI Abstract Summarization of this paper

### 3.2 Glossary Creation for Technical Terms
> Verify, Give me all the AI terms in markdown format as Glossary used in this paper, to make it understandable. sharing sample Glossary for your reference. 

#### Sample Glossary Structure Provided:
```markdown
## Complete Glossary 

### Core Concepts

**Token** 
A small piece of text (word or part of a word) that the model processes. Examples: "Hello" → 1 token, "understand" → might be 2 tokens ("under" + "stand").

### Architecture Components 

**Transformer** 
A neural network architecture used in modern language models (GPT, Llama) that processes tokens using attention and feed-forward layers.
```

---

## 4. Utility Tools & Resources
Non-prompt content providing additional functionality.

### 4.1 YouTube Timestamp Extraction Regex
> This is not a prompt, to replace youtube timing from summaries.

**Pattern 1 - Time Ranges:**
```regex
\(\s*(\d{1,2}:\s*\d{2}(\s*[-,]?\s*\d{1,2}:\s*\d{2})*)\s*\)
```

**Pattern 2 - Reference Markers:**
```regex
\.\[\d+\](?:\s*\[\d+\])*$
```

