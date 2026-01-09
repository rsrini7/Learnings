# DSPy: The End of Prompt Engineering

---

## TABLE OF CONTENTS
1. [Introduction & Key Concepts](#introduction--key-concepts)
2. [Core DSPy Primitives (6 Concepts)](#core-dspy-primitives-6-concepts)
3. [Detailed Component Breakdown](#detailed-component-breakdown)
4. [Real-World Use Cases](#real-world-use-cases)
5. [Code Examples & Implementation](#code-examples--implementation)
6. [Optimizers: The Game-Changer](#optimizers-the-game-changer)
7. [Q&A Highlights](#qa-highlights)
8. [Key Takeaways](#key-takeaways)

---

## INDEX OF CONCEPTS

- **Adapters**: Prompt formatters (JSON, BAML, XML)
- **Attachments**: File handling library for multimodal content
- **Boundary Detection**: Finding logical sections in structured documents
- **Chain of Thought**: Module for step-by-step reasoning
- **Convenience**: Abstraction that handles implementation details
- **Declarative Programming**: Expressing intent, not implementation
- **Metrics**: Quantitative success measures for optimization
- **Modules**: Logical program components using signatures
- **Multimodality**: Support for images, audio, text, PDFs
- **Optimizers**: Automatic prompt tuning (MIPRO, Bayesian)
- **Program with Thought**: Code reasoning module
- **ReAct**: Tool-calling module
- **Signatures**: Input/output specifications
- **Tools**: Python functions exposed to LLM
- **Transferability**: Moving between models without rewriting
- **Type Safety**: Guaranteed input/output contracts

---

## INTRODUCTION & KEY CONCEPTS

### The Core Philosophy: "Program with LLMs, Not Just Prompt Engineering"

**The Challenge:**
- Enterprise applications need to be rigorous, testable, and robust
- LLMs make this challenging because they're inherently non-deterministic
- Traditional "prompt engineering" (tweaking strings) doesn't scale

**The Solution: DSPy**
- Declarative framework for building modular software with LLMs
- Shifts from **brittle prompt tweaking** → **structured programming with LLM components**
- Treats LLMs as first-class citizens in code

### Why DSPy (The Advantages)

#### 1. **Abstraction Level**
- Sits at a "sweet spot" between too high-level (LangChain) and too low-level
- Doesn't get in your way
- Lets you focus on what matters, not implementation details

#### 2. **Programs Over Prompts**
- Build proper Python programs, not just prompt strings
- Structured, testable code instead of manual tweaking
- Type safety and input/output guarantees

#### 3. **Systems Mindset (from Omar - DSPy Creator)**
- Encodes your intent in a transferable, modular way
- Program structure remains stable as model capabilities evolve
- Bounce between models without rewriting your logic

#### 4. **Convenience**
- No manual JSON parsing
- No string construction headaches
- Retain precision while abstracting away boilerplate

#### 5. **Model & Paradigm Flexibility**
- Keep your program logic intact
- Swap models as new ones release (daily in current landscape)
- Transferability across different LLM architectures

#### 6. **Comparable to Other Solutions**
- Other great libraries exist: Pydantic, LangChain, Anthropic SDK, Agno
- DSPy is one perspective, not the only option
- Has a set of primitives that fit together cohesively

---

## CORE DSPY PRIMITIVES (6 CONCEPTS)

### The Six Core Primitives:

```
1. SIGNATURES      → Define inputs/outputs (what you want to do, not how)
2. MODULES         → Logical structure (how you organize your code, based on PyTorch methodology)
3. TOOLS           → Python functions (enable LLM to take action) exposed to the LLM.
4. ADAPTERS        → Prompt formatters (JSON vs BAML vs XML), sitting between the signature and the LLM.
5. OPTIMIZERS      → Automatic prompt tuning (the "killer feature"). Quantitative improvement of performance.
6. METRICS         → Success measurement (feedback for optimizers)
```

---

## DETAILED COMPONENT BREAKDOWN

### 1. SIGNATURES - Declaring Intent

**Purpose:** Specify what you want an LLM function call to do, Signatures define the "contract" for the LLM.

#### Two Forms:

#### A. Shorthand Signature (String-Based)
```python
"text -> sentiment: int"
```
- **Simplest approach**
- Defers implementation to DSPy and the model
- Great for rapid experimentation
- Example: "given text, output sentiment as integer"

#### B. Class-Based Signature (Pydantic-Like)
```python
class SentimentClassifier(dspy.Signature):
    """Classify the sentiment of the text."""
    text: str = dspy.InputField()
    sentiment: int = dspy.OutputField(
        desc="Sentiment: 0=very negative, 5=neutral, 10=very positive"
    )
```

**Key Insight: Field Names Are Part of the Prompt**
- The names themselves act as "mini-prompts"
- Intuitive naming helps the model understand what you want
- These become part of the actual prompt sent to the LLM

**Example Real Use Case:**
```python
class TimeEntryFormatter(dspy.Signature):
    """Format and standardize time entry descriptions."""
    entry: str = dspy.InputField(
        desc="Raw time entry from legacy system"
    )
    formatted_entry: str = dspy.OutputField(
        desc="Properly capitalized, period-terminated entry"
    )
```
- Client had 100,000+ time entries requiring standardization
- Used DSPy to elegantly enforce format standards

**Handling Existing Prompts:**
- If you already have a great prompt, you can inject it via docstring
- Use `description` field for additional context
- System instructions can be added at various points
- Doesn't prevent you from using proven prompts as a starting point

---

### 2. MODULES - Logical Organization

**Purpose:** Organize program logic using LLM components as building blocks, Modules wrap signatures with specific strategies.

#### Basic Structure:
```python
class TimeEntryModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.format_entry = dspy.ChainOfThought(TimeEntryFormatter)
    
    def forward(self, entry):
        # Call the LLM component
        result = self.format_entry(entry=entry)
        
        # Add custom business logic
        if len(result.formatted_entry) > 200:
            result.formatted_entry = result.formatted_entry[:200] + "..."
        
        return result
```

#### Key Characteristics:
- Based on PyTorch-like methodology (initialization + forward method)
- Contain one or more signatures
- Can include additional business logic
- Composable: modules can contain other modules
- **Modules allow you to inline LLM calls with hard-coded logic**

#### Built-in Modules (Collection of Prompting Techniques):

1. **dspy.Predict** (The Worker)

   - **Vanilla LM call:** Just sends your inputs to the model and gets an output.
   - **No special technique:** It doesn't add "Step by step" or "Think about it."
   - **Initialization:** You define it once in the `__init__` section of your class. Just like a linear layer in PyTorch.
   - **Optimizer Benefit:** This is crucial for the **Optimizer**. Because the predictor is an attribute of the class, the DSPy optimizer can find it, "compile" it, and rewrite its internal prompt instructions to improve performance.

2. **dspy.Prediction** (The Result)

   - **Data Container:** It is just a fancy Python dictionary that holds the model's output.
   - **Dot-access:** It lets you type `result.answer` instead of `result['answer']`.
   - **Return Type:** You use this in the `forward` function to return the final answer so other parts of DSPy can read it easily.
   - **Traceability:** It preserves the "reasoning" and metadata (like token usage) that DSPy tracks under the hood
   - **Consistency:** It ensures that your custom module returns the same type of object as built-in DSPy modules, making your code "composable"

   ##### **Predict vs Prediction**

    | Feature | `dspy.Predict` | `dspy.Prediction` |
    | --- | --- | --- |
    | **Location** | `__init__` | `forward` |
    | **Type** | Module / Layer | Data Container / Result |
    | **Purpose** | Defines *how* to process data | Holds the *final result* |
    | **Analogy** | A specialized worker | The envelope containing the work |

3. **dspy.ChainOfThought** (The Reasoning Worker)

   - **Adds reasoning steps:** This is what actually adds "Let's think step by step" to your prompt.
   - **Smart Wrapper:** It is a more advanced version of `dspy.Predict`.
   - **Implicit logic:** It forces the model to generate a "Rationale" field before giving the final answer.


    ##### Comparison at a Glance

    | Feature | `dspy.Predict` | `dspy.ChainOfThought` | `dspy.Prediction` |
    | --- | --- | --- | --- |
    | **What is it?** | A Module (Execution) | A Module (Execution) | An Object (Data) |
    | **Prompting** | Direct/Simple | Reasoning/CoT | None (it's just data) |
    | **Where it lives** | `__init__` | `__init__` | `forward` (return) |


4. **dspy.ReAct** (Tool Calling) **dspy.CodeAct** (Code)
   - Exposes Python functions to the model as tools (like search/APIs)
   - How DSPy handles tool/function calling
   - Wraps signatures and injects tools for agent-like behavior
   - Execute code for external data/actions

5. **dspy.ProgramWithThought**
   - Deterministic, high-precision, or complex calculations performed by generated code
   - Forces model to reason in code
   - Returns code execution result
   - Comes with Python interpreter built-in
   - Customizable with your own execution harness
   - Great for highly technical problems

6. **dspy.Retrieve**
   - For retrieval-based approaches
   - Part of RAG pipelines

7. **dspy.MultiChainComparison** (or) **dspy.BestOfN**
   - Compare multiple outputs
   - Parallel execution patterns

8. **dspy.Refine**
   - Refine output based on feedback
   - Iterative improvement

9. **dspy.Reason**
   - Reasoning module
   - Adds reasoning steps
   - "Let's think step by step"
   - Relevant when model benefits from explicit reasoning

10. **dspy.Parallel**
   - To process multiple items

11. **dspy.Select**
    - Select the best output
    - Parallel execution patterns

#### Philosophy:
- Just being able to logically separate components has been powerful
- Added benefit: end result is inherently optimizable
- This is why modules matter, separate from optimizers

---

### 3. TOOLS - Function Exposure

**Purpose:** Give LLMs access to Python functions for action-taking

#### Implementation:
```python
@dspy.tool
def get_weather(location: str) -> str:
    """Get current weather for a location."""
    # Implementation
    return weather_data

@dspy.tool
def search_web(query: str) -> list[str]:
    """Search the web for query."""
    # Implementation
    return results

# Create an agent
agent = dspy.ReAct(dspy.Signature("question -> answer: str"))
agent.set_tools([get_weather, search_web])

# Call it
result = agent(question="What's the weather like in Tokyo?")
```

#### Key Points:
- Simply wrap Python functions
- DSPy uses LightLLM under the hood for coupling
- Tools work seamlessly within modules
- ReAct paradigm handles tool calling orchestration
- Can limit rounds (e.g., max_hops=5) to prevent infinite loops

---

### 4. ADAPTERS - Prompt Formatting

**Purpose:** Translate signatures and inputs into the actual prompt format sent to LLM, Adapters allow you to change how the model "sees" the instructions without changing your code.

#### The Pipeline:
```
Signature + Inputs 
    ↓
[ADAPTER]
    ↓
Formatted Prompt (JSON/BAML/XML/etc)
    ↓
LLM
```

#### Types of Adapters:

**A. JSON Adapter (Default)**
```
Input specification with field names
{
  "clinical_note": "Patient presented with...",
  "patient_info": {
    "name": "John",
    "age": 45,
    "conditions": ["diabetes", "hypertension"]
  }
}
Output specification with requested fields
```

**B. BAML Adapter (More Efficient)**
```
clinical_note: "Patient presented with..."

patient_info:
  name: "John"
  age: 45
  conditions:
    - diabetes
    - hypertension
```

#### Performance Comparison:
- BAML formatting is slightly more intuitive for humans
- **5-10% performance improvement** depending on use case
- More token-efficient than verbose JSON
- Same program logic, just change the adapter

#### Flexibility:
- Research shows different models perform differently with different formats
- XML, BAML, JSON all have merits
- Adapters let you mix-and-match without changing program logic
- Easy to A/B test different formatting strategies

---

### 5. MULTIMODALITY Support

**Purpose:** Handle multiple input types (images, audio, text, PDFs, documents)

#### Features:
- Natively supports images, audio, and other modalities
- Simple to integrate into signatures
- Works seamlessly with output processing

#### Tool: Attachments Library
```python
from dspy_attachments import Attachments

# Pull in a PDF with one line
doc = Attachments.from_url("https://example.com/form4.pdf")

signature = dspy.Signature(
    "document -> key_info: str"
)

result = dspy.Predict(signature)(document=doc)
```

**Created by**: Maxim (another DSPy enthusiast)
- Catch-all library for working with different file types
- Converts PDFs, images, documents to LLM-friendly format
- Handles OCR and preprocessing automatically
- Makes working with multimodal content incredibly simple

#### Example Use Case: SEC Filing Analysis
```python
# Simple RAG over a PDF
form4_pdf = Attachments.from_url(nvidia_form4_url)

signature = dspy.Signature(
    "document, question -> answer: str"
)

# Query the document
result = dspy.Predict(signature)(
    document=form4_pdf,
    question="How many shares were sold?"
)

# Output handles complex reasoning
# Finds two transactions, does math, provides answer
```

---

### 6. OPTIMIZERS - Automatic Prompt Tuning

**Purpose:** Automatically improve prompt effectiveness to achieve better results, Optimizers use AI to improve AI.

#### Key Philosophy:
> **"DSPy is NOT an optimizer. DSPy is a set of programming abstractions. You just happen to be able to optimize it."** - Omar, DSPy Creator

#### What Optimizers Actually Do:
- Iteratively prompt and tweak the prompt under the hood
- Find the "nooks and crannies" in the model behavior
- Leverage adversarial examples (what Carpathy discussed) but for optimization
- Work across different models and use cases

#### Why Optimizers Matter:

**Use Case Example: Cost Optimization**
```
Scenario: Classification works great with GPT-4
- Performance: 92%
- Cost: High (runs 1M times/day)

Switch to GPT-4 Mini:
- Performance: 70% (unacceptable)

Run MIPRO Optimizer on GPT-4 Mini:
- Performance: 87% (acceptable for use case!)
- Cost: 10x cheaper

Result: Keep the program logic, drop costs by orders of magnitude
```

#### The Optimizer Advantage:
- **Transferability**: Same program, different models, automatic optimization
- **In-context Learning**: Research shows it's competitive with fine-tuning
- **No Infrastructure**: Try this first before complex fine-tuning pipelines
- **Composable**: Optimizes multiple modules together

#### The Adversarial Example Connection:
From Dwaresh and Carpathy:
- Using LLM as judge can be exploited (model finds adversarial examples)
- Optimizers flip this on its head: use this property to find improvements
- Model naturally finds the spots where performance can improve
- Systematic exploitation of these "cracks" for optimization

#### How It Works:

```
1. Construct Program
   ├─ Define signatures
   ├─ Create modules
   └─ Connect components

2. Create Dataset & Metrics
   ├─ Training examples with expected outputs
   └─ Metric function (e.g., exact match, semantic similarity)

3. Run Optimizer (e.g., MIPRO)
   ├─ Tests different prompts
   ├─ Measures against your metric
   └─ Iteratively improves

4. Get Compiled Module
   └─ Same code structure, optimized prompts
```

---

### 7. METRICS - Defining Success

**Purpose:** Quantitatively measure if your program is working, Metrics are the "building blocks" of success.

#### How Metrics Work:
```python
def time_entry_accuracy(expected, predicted, trace=None):
    """Return 0 or 1 based on exact match."""
    return int(expected == predicted)

def semantic_similarity(expected, predicted, trace=None):
    """Return 0-1 based on semantic match."""
    return embedding_similarity(expected, predicted)
```

#### Used By Optimizers:
- Optimizers use metrics to determine if changes improve performance
- Drives the optimization direction
- Essential for measurable improvement

---

## REAL-WORLD USE CASES

### Use Case 1: Time Entry Standardization

**Problem:**
- Client had 100,000+ manually entered time entries
- Different formats, capitalizations, punctuation
- Needed standardization without losing information

**Solution:**
```python
class TimeEntryFormatter(dspy.Signature):
    """Standardize and format time entry descriptions."""
    entry: str = dspy.InputField(desc="Raw entry")
    formatted_entry: str = dspy.OutputField(desc="Properly formatted")

class TimeEntryModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.formatter = dspy.Predict(TimeEntryFormatter)
    
    def forward(self, entry):
        return self.formatter(entry=entry)
```

**Why DSPy Was Perfect:**
- Declarative approach to a simple but important problem
- Easy to test and iterate on format requirements
- Could apply business logic rules after LLM processing
- Eventually optimized the prompts automatically

---

### Use Case 2: PDF Document Classification (File Routing)

**Problem:**
- Need to route arbitrary files (SEC filings, contracts, invoices) to appropriate processors
- Each document type requires different handling

**Solution:**
```python
class DocumentRouter(dspy.Module):
    def __init__(self):
        super().__init__()
        self.classifier = dspy.ReAct(
            dspy.Signature(
                "document -> classification: str"
            )
        )
        self.classifier.set_tools([
            analyze_structure,
            extract_metadata,
            identify_signatures
        ])
    
    def forward(self, document):
        result = self.classifier(document=document)
        return self.route_based_on_classification(result)
```

**Features:**
- Uses ReAct for tool-calling capabilities
- Analyzes document structure
- Extracts metadata
- Routes to appropriate pipeline

---

### Use Case 3: Visual Boundary Detection in PDFs

**Problem:**
- Legal documents have complex layouts with multiple sections
- Need to detect logical boundaries within visually-structured documents
- Visual layout matters more than text alone

**Solution:**
```python
class BoundaryDetector(dspy.Module):
    def __init__(self):
        super().__init__()
        self.detector = dspy.Predict(
            dspy.Signature(
                "pdf_images, page_number -> boundaries: list[int]"
            )
        )
    
    def forward(self, pdf_document):
        # Get images from PDF (via Attachments)
        pages = Attachments.from_pdf(pdf_document)
        
        results = []
        for page_num, page_image in enumerate(pages):
            boundaries = self.detector(
                pdf_images=page_image,
                page_number=page_num
            )
            results.extend(boundaries)
        
        return self.merge_boundaries(results)
```

**Key Insight:**
- Multimodal input (images) captures visual structure
- Model understands layout better from images than text
- Critical for documents with complex formatting

---

### Use Case 4: Sentiment Classification

**Simplest Example:**
```python
# Shorthand signature - minimal setup
class SentimentClassifier(dspy.Module):
    def __init__(self):
        super().__init__()
        self.classifier = dspy.Predict("text -> sentiment: int")
    
    def forward(self, text):
        return self.classifier(text=text)

# Usage
classifier = SentimentClassifier()
result = classifier(text="This product is amazing!")
```

**Features:**
- Dead simple for quick experimentation
- Can start with shorthand, upgrade to full signatures
- Perfect for rapid prototyping

---

### Use Case 5: Simple Web Research Agent

```python
class ResearchAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.agent = dspy.ReAct(
            dspy.Signature(
                "question -> research_summary: str"
            ),
            num_hops=5
        )
        self.agent.set_tools([search_web, get_news])
    
    def forward(self, query):
        return self.agent(question=query)
```

**Key Features:**
- Tool calling via ReAct
- Limited hops (5) prevents runaway loops
- Can search and aggregate results

---

### Use Case 6: Text Summarization (Arbitrary Length)

**Problem:**
- Need to summarize variable-length documents
- Standard LLMs have context limitations

**Solution:**
```python
class TextSummarizer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarizer = dspy.Predict(
            dspy.Signature(
                "text -> summary: str"
            )
        )
    
    def forward(self, text):
        if len(text) > context_limit:
            # Split and recursively summarize
            chunks = self.chunk_text(text)
            summaries = [self.summarizer(text=chunk) for chunk in chunks]
            return self.summarizer(text=" ".join(summaries))
        else:
            return self.summarizer(text=text)
```

---

## CODE EXAMPLES & IMPLEMENTATION

### Example 1: Class-Based Signature (Full Definition)

```python
class PatientInfoExtractor(dspy.Signature):
    """Extract patient information from clinical notes."""
    
    clinical_note: str = dspy.InputField(
        desc="Raw clinical note text"
    )
    patient_details: dict = dspy.InputField(
        desc="Structured patient metadata"
    )
    
    extracted_info: dict = dspy.OutputField(
        desc="Extracted and validated patient info"
    )
    confidence: float = dspy.OutputField(
        desc="Confidence score 0.0-1.0"
    )
```

**In the Actual Prompt:**
```
Input Fields:
- clinical_note (string): Raw clinical note text
- patient_details (object): {name, age, conditions...}

Output Fields:
- extracted_info (object): Extracted and validated patient info
- confidence (float): Confidence score 0.0-1.0
```

---

### Example 2: Module with Business Logic

```python
class SecFilingAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.extractor = dspy.Predict(
            dspy.Signature(
                "filing -> shares_sold: int, transaction_dates: list"
            )
        )
    
    def forward(self, filing_document):
        # Call LLM component
        result = self.extractor(filing=filing_document)
        
        # Add validation logic
        if result.shares_sold < 0:
            result.shares_sold = 0
        
        # Add calculation logic
        result.days_between_transactions = (
            self._calculate_days(result.transaction_dates)
        )
        
        return result
    
    def _calculate_days(self, dates):
        if len(dates) >= 2:
            return (dates[-1] - dates[0]).days
        return 0
```

---

### Example 3: Adapter Usage

```python
# Create signature
class DataExtractor(dspy.Signature):
    document: str = dspy.InputField()
    extracted_data: dict = dspy.OutputField()

# Use with different adapters
json_module = dspy.Predict(DataExtractor)
json_module.set_adapter(dspy.adapters.JSONAdapter)

baml_module = dspy.Predict(DataExtractor)
baml_module.set_adapter(dspy.adapters.BAMLAdapter)

# Same logic, different prompt formatting
json_result = json_module(document=doc)
baml_result = baml_module(document=doc)

# Compare performance and choose
```

---

### Example 4: Complete RAG Pipeline (Simple)

```python
class SimpleRAGPipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.qa = dspy.Predict(
            dspy.Signature(
                "context, question -> answer: str"
            )
        )
    
    def forward(self, document_url, question):
        # Pull document with Attachments
        doc = Attachments.from_url(document_url)
        
        # Query directly
        result = self.qa(context=doc, question=question)
        
        return result

# Usage example from talk
rag = SimpleRAGPipeline()
answer = rag(
    document_url="nvidia_form4.pdf",
    question="How many shares were sold?"
)
# Returns: "427,500 shares" (handles multiple transactions + math)
```

---

## OPTIMIZERS: THE GAME-CHANGER

### Complete Optimizer Workflow

#### Step 1: Define Your Program
```python
class MyProgram(dspy.Module):
    def __init__(self):
        super().__init__()
        self.step1 = dspy.Predict(Step1Signature)
        self.step2 = dspy.Predict(Step2Signature)
        self.step3 = dspy.Predict(Step3Signature)
    
    def forward(self, input_data):
        result1 = self.step1(data=input_data)
        result2 = self.step2(data=result1)
        result3 = self.step3(data=result2)
        return result3
```

#### Step 2: Create Dataset with Expected Outputs
```python
training_set = [
    {
        "input": "example input 1",
        "expected_output": "expected output 1"
    },
    {
        "input": "example input 2",
        "expected_output": "expected output 2"
    },
    # ... more examples
]
```

#### Step 3: Define Metric Function
```python
def my_metric(example, pred, trace=None):
    """
    Return 1 if prediction matches expected, 0 otherwise.
    Trace parameter gives access to intermediate steps.
    """
    expected = example.expected_output
    actual = pred.output_field
    
    # Exact match
    return int(expected == actual)

# Or for more nuanced scoring
def semantic_metric(example, pred, trace=None):
    expected = example.expected_output
    actual = pred.output_field
    
    similarity = calculate_embedding_similarity(expected, actual)
    return similarity  # Returns 0.0-1.0
```

#### Step 4: Create and Run Optimizer
```python
from dspy.optimizers import MIPROv2  # or BayesianSignatureOptimizer, etc.

optimizer = MIPROv2(
    metric=my_metric,
    num_batches=10,
    max_bootstrapped_demos=4
)

# Compile your program
compiled_program = optimizer.compile(
    student=MyProgram(),
    trainset=training_set,
    valset=validation_set,
)

# Use compiled program
result = compiled_program(input_data)
```

### Example: Optimizer Results (From Talk)

**Time Entry Correction Use Case:**
- Initial performance (manual prompt): 86%
- After MIPRO optimization: 89%
- Improvement: +3% with same model
- Key insight: Optimizer found better ways to phrase instructions

---

## Q&A HIGHLIGHTS

### Q: "I Already Have a Great Prompt"

**Kevin's Answer:**
- You can absolutely use your existing prompt
- Inject it via the docstring field
- Use description field for additional context
- Wrap custom prompts in methods to apply system instructions
- Doesn't prevent you from having a super-prompt
- Can serve as great starting point for optimization

---

### Q: "Is RAG Creating a Vector Store?"

**Kevin's Answer:**
- In the example, it's "poor man's RAG"
- Just pulling in document images/text
- Attachments does basic OCR
- Rest is fed directly to model
- **Not** doing vector embeddings or semantic search
- Good for smaller documents; vector RAG when you need scale

---

### Q: "How Does This Handle Delayed Feedback & Online Learning?"

**Kevin's Answer:**
- Optimizers can be retrained on new data
- In production, you'd collect examples
- Periodically rerun optimizer with new/updated dataset
- Online learning scenarios would require custom setup
- Framework is flexible enough but not native feature

---

## KEY TAKEAWAYS

### 1. **Programming Paradigm Shift**
- Stop thinking "prompt engineering" → Start thinking "programming with LLMs"
- Treat prompts as implementation details, not core logic
- Define intent through signatures, let system handle the rest

### 2. **Modularity Enables Optimization**
- Breaking code into modules = prerequisite for optimization
- Even without optimization, modularity is valuable
- Logical separation of concerns pays dividends

### 3. **Transferability is Real**
- Same program structure works across different models
- Optimize once, swap models freely
- Cost and capability tradeoffs become manageable

### 4. **DSPy Isn't The Only Answer**
- Great alternatives exist (Pydantic, LangChain, Anthropic SDK)
- DSPy is one perspective
- Try it, test it with your use cases

### 5. **Start Simple, Scale Gracefully**
- Shorthand signatures for quick prototyping
- Graduate to class-based signatures
- Add optimizers when you need scale

### 6. **Optimizers Are Optional (But Powerful)**
- Value comes first from programming abstractions
- Optimizers are incredible added benefit
- Don't require optimizers to benefit from DSPy

### 7. **Practical Applicability**
- Works for real client problems (time entries, documents, SEC filings)
- Elegant handling of complex tasks
- Observable improvements through metrics

### 8. **The Systems Mindset**
- Design with transferability in mind
- Encode intent expressively
- Let the system optimize and adapt

---

## REPOSITORY & RESOURCES

**GitHub Repository** (mentioned in talk):
- Contains all code examples from the talk
- Use cases: sentiment classifier, PDF processing, multimodal work, web agent, boundary detection, text summarization, optimizer examples
- Utilities and demonstrations (not production code)
- Available for download and local experimentation

**Key Contributors & Resources:**
- **Omar (Omar Al Khabib)** - DSPy Creator
  - A16Z Podcast interview (2 days before talk)
  - Core vision of DSPy

- **Gajanan Pashant** - Adapter Research
  - Twitter handle referenced
  - JSON vs BAML comparison studies

- **Maxim** - Attachments Library Creator
  - Created library for easy file handling
  - Twitter: @maxim

- **Chris Pototts** - DSPy Related Work
  - Recent talks on related concepts

- **Kevin Madura**
  - Twitter: @kmad
  - Available for questions/discussion

---

## CONCLUSION

**The Bottom Line:**
> "DSPy is really all you need" - not because it's the only option, but because it provides a cohesive, principled way to build LLM applications that are modular, testable, optimizable, and transferable.

The shift from "tweaking prompts" to "programming with LLMs" isn't just about better results—it's about bringing software engineering rigor to AI application development. DSPy enables this paradigm shift through elegant abstractions that don't get in your way.

---

## Reference

https://www.youtube.com/watch?v=-cKUW6n8hBU
https://github.dev/kmad/aie

| Person          | Resource            | Link/Reference                                                |
| --------------- | ------------------- | ------------------------------------------------------------- |
| Omar Al Khabib  | DSPy Creator        | A16Z Podcast (2 days before talk)                             |
| Gajanan Pashant | Adapter Research    | Twitter handle referenced for JSON vs BAML comparison studies |
| Maxim           | Attachments Library | Twitter: @maxim (file handling library creator)               |
| Chris Pototts   | DSPy Related Work   | Recent talks on related concepts                              |
| Kevin Madura    | Speaker             | Twitter: @kmad (available for questions)                      |