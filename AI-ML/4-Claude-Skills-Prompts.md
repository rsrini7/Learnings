Explore more on : [https://agentskills.so/](https://agentskills.so/)


### Use Case 1. Lead Scoring Calculator Prompt

Create a Skill called "Lead Scoring Calculator" that does the following:

PURPOSE:
Generate an Excel spreadsheet that scores and ranks leads based on customizable criteria.

INPUTS THE SKILL SHOULD REQUEST:
1. List of leads with their details (name, company, relevant data points)
2. Scoring criteria with weights (or use defaults if not provided)

DEFAULT SCORING CRITERIA (if user doesn't specify):
- Company Size: 20 points max (1-10 employees = 5pts, 11-50 = 10pts, 51-200 = 15pts, 200+ = 20pts)
- Budget: 30 points max ($10K-25K = 10pts, $25K-50K = 20pts, $50K+ = 30pts)
- Timeline: 25 points max (Just researching = 5pts, 3-6 months = 15pts, Ready now = 25pts)
- Industry Fit: 15 points max (Poor fit = 0pts, Okay fit = 8pts, Perfect fit = 15pts)
- Engagement Level: 10 points max (Cold = 2pts, Warm = 6pts, Hot = 10pts)

OUTPUT:
Create an Excel file with these columns:
- Lead Name
- Company
- Company Size Score
- Budget Score
- Timeline Score
- Industry Fit Score
- Engagement Score
- TOTAL SCORE (sum of all scores)
- PRIORITY RANK (1 = highest score)

FORMATTING:
- Sort by Total Score (highest to lowest)
- Add conditional formatting: 
  * Green fill for scores 70+
  * Yellow fill for scores 50-69
  * Red fill for scores below 50
- Bold the column headers
- Auto-fit column widths
- Include a summary at the top showing: Total Leads, Avg Score, # of Hot Leads (70+)

Make the Skill friendly and ask clarifying questions if the lead data provided is unclear.

​

### Use Case 2. Client Report Builder Skill Prompt

- A Claude Skill that generates an Excel spreadsheet that scores and ranks leads based on customizable criteria. Copy and customize as you see fit.

A Claude Skill that reads project files from a specified folder on your computer and generates a comprehensive, formatted PDF report suitable for client delivery. Copy and customize as you see fit.

Create a Skill called "Client Report Builder" that generates professional PDF client reports.

PURPOSE:
Read project files from a specified folder on my computer and generate a comprehensive, formatted PDF report suitable for client delivery.

THE SKILL SHOULD:

1. ASK THE USER FOR:
   - Path to the project folder
   - Client name (if not in files)
   - Report date

2. READ these files from the folder:
   - project-data.txt (project details, objectives, deliverables)
   - metrics.csv (performance data)
   - notes.txt (wins, challenges, feedback)

3. GENERATE A PDF with these sections:

   **COVER PAGE:**
   - Client name (large, prominent)
   - Project title
   - Report date
   - "Prepared by [Your Name/Company]"

   **EXECUTIVE SUMMARY (1 page):**
   - Brief project overview (2-3 sentences)
   - Key achievements (3-4 bullet points, data-driven)
   - Overall assessment (success level, notable wins)

   **PROJECT OVERVIEW:**
   - Objectives (bulleted list from project-data.txt)
   - Deliverables completed (formatted list)
   - Timeline and scope

   **RESULTS & METRICS:**
   - Create a formatted table from metrics.csv
   - Include: Metric name, Target, Actual, Variance
   - Add brief analysis highlighting top 3 performing metrics

   **KEY WINS:**
   - Extract from notes.txt
   - Format as scannable bullets
   - Include supporting data where available

   **CHALLENGES & SOLUTIONS:**
   - Extract challenges from notes.txt
   - Frame positively (what was learned, how it was handled)

   **CLIENT FEEDBACK:**
   - Direct quote from notes.txt (formatted as blockquote)

   **RECOMMENDATIONS & NEXT STEPS:**
   - Based on all data, suggest 3-5 concrete next steps
   - Focus on: what worked (do more), opportunities for improvement, logical expansions
   - Include estimated timelines or resource needs if relevant

   **APPENDIX (optional):**
   - Full metrics table
   - Detailed deliverables list

FORMATTING REQUIREMENTS:
- Professional business style (clean, scannable)
- Use headings and subheadings
- Include page numbers
- Add whitespace for readability
- Metrics table should be clearly formatted
- Bullet points for lists
- Bold key numbers and achievements

The Skill should be conversational and confirm the folder path before reading files.

If files are missing or unreadable, provide helpful error messages.

​

### Use Case 3. Survey Data Analyzer Skill Prompt

- A Skill that acts as a strategic business decision-making partner that helps entrepreneurs evaluate options using proven frameworks. Customize as you see fit.

Create a Claude Skill (SKILL.md file) for strategic business decision-making that helps entrepreneurs evaluate options using proven frameworks.

The skill should:

1. Apply multiple decision-making frameworks simultaneously:
   - First Principles Thinking (break down to fundamental truths)
   - Pareto's 80/20 Rule (identify highest-leverage actions)
   - Systems Thinking (understand interconnections and second-order effects)
   - Jobs-to-Be-Done (understand what outcome the user is actually trying to achieve)

2. For every decision analysis, provide:
   - Clear recommendation with justification
   - Alternative approaches considered
   - Potential blind spots or risks
   - Impact on profit margins (when relevant)
   - Trade-offs between options
   - Second-order consequences

3. Structure responses as:
   - **The Real Question**: Reframe using Jobs-to-Be-Done
   - **First Principles Analysis**: Break down assumptions
   - **80/20 Assessment**: Identify highest-leverage path
   - **Systems View**: Map interconnections and ripple effects
   - **Recommendation**: Clear position with reasoning
   - **Alternatives**: Other viable paths
   - **Blind Spots**: What could go wrong
   - **Decision Framework**: How to evaluate success

4. Tone and approach:
   - Direct and intellectually honest
   - Challenge assumptions when warranted
   - Provide specific critique, not generic praise
   - Use plain language, avoid buzzwords
   - Take clear positions rather than hedging
   - Ask one high-impact question rather than many shallow ones

5. For business decisions, always consider:
   - Time investment required
   - Profit margin impact
   - Scalability potential
   - Compounding vs. one-time value
   - Opportunity cost
   - Alignment with strategic goals

The skill should help users make faster, better-informed decisions by systematically applying multiple frameworks rather than relying on intuition alone.

Format the output as a complete SKILL.md file ready to be uploaded to Claude.

​

### Use Case 4. Survey Data Analyzer Skill Prompt

- This Skill transforms raw survey data into actionable insights with multiple formatted outputs: summary report, visualizations, key findings, and recommendations. Copy and customize as you see fit.

Create a Skill called "Survey Data Analyzer" that reads survey response CSVs and generates comprehensive analysis deliverables.

PURPOSE:
Transform raw survey data into actionable insights with multiple formatted outputs: summary report, visualizations, key findings, and recommendations.

THE SKILL SHOULD:

1. ASK THE USER FOR:
   - Path to the survey CSV file
   - Survey context (what was the survey about, who responded)
   - Specific focus areas (if any)

2. READ AND ANALYZE the CSV:
   - Parse all responses
   - Calculate rating distributions
   - Identify themes and patterns in open-ended responses
   - Categorize feedback by topic
   - Flag common pain points and requests
   - Detect sentiment trends

3. GENERATE FOUR OUTPUTS:

   **OUTPUT 1: Executive Summary Report (Word Doc)**
   Create a professional document with:
   
   SECTION: Survey Overview
   - Number of responses
   - Date range
   - Response rate (if known)
   - Survey context
   
   SECTION: Key Metrics
   - Average satisfaction score
   - Score distribution (% in each rating band)
   - Response completion rate
   
   SECTION: Top Themes
   - 5-7 most common themes from qualitative feedback
   - % of respondents mentioning each theme
   - Representative quotes (2-3 per theme)
   
   SECTION: Critical Insights
   - What's working well (positive patterns)
   - What needs attention (pain points)
   - Surprising or unexpected findings
   
   SECTION: Sentiment Analysis
   - Overall sentiment (positive/neutral/negative breakdown)
   - Tone patterns in feedback
   
   **OUTPUT 2: Data Visualization Sheet (Excel)**
   Create spreadsheet with:
   
   TAB 1: Rating Distribution
   - Bar chart showing count of each rating (1-10)
   - Calculate: Mean, Median, Mode
   - Net Promoter Score (if 1-10 scale)
   
   TAB 2: Theme Frequency
   - Table: Theme | Count | Percentage | Sample Quotes
   - Horizontal bar chart of theme frequency
   
   TAB 3: Area Breakdown
   (if survey asks about business areas)
   - Count by category (Content, Lead Gen, Operations, etc.)
   - Pie chart showing distribution
   
   TAB 4: Word Cloud Data
   - Top 50 most frequent words from open responses
   - Frequency count for each word
   - Exclude common stop words
   
   **OUTPUT 3: Key Findings Document (PDF)**
   Create a scannable, visual 1-pager with:
   
   TOP SECTION: At A Glance
   - Big number: Average Score
   - Big number: Total Responses
   - Big number: % Would Recommend
   
   FINDINGS (Bullet format):
   ✓ What We're Doing Right (3 bullets)
   ⚠ Areas for Improvement (3 bullets)
   💡 Opportunities Identified (3 bullets)
   
   QUOTES CALLOUT:
   - 2-3 powerful direct quotes in highlighted boxes
   
   **OUTPUT 4: Action Plan Presentation (PowerPoint)**
   Create 8-10 slide deck:
   
   Slide 1: Title
   - Survey Results & Recommendations
   - Date, # Responses
   
   Slide 2: Executive Summary
   - Key numbers, overall takeaway
   
   Slide 3: Satisfaction Overview
   - Rating distribution chart
   - Trend vs previous surveys (if applicable)
   
   Slide 4-6: Top Themes (1 slide per theme)
   - Theme name
   - % mentioned
   - 2-3 supporting quotes
   - Visual icon/graphic
   
   Slide 7: What to Stop/Start/Continue
   - Based on feedback patterns
   
   Slide 8: Priority Recommendations
   - Top 5 action items
   - Each with: What, Why, Expected Impact
   
   Slide 9: Implementation Roadmap
   - Timeline: Quick wins (30 days), Medium-term (90 days), Long-term (6+ months)
   
   Slide 10: Next Steps
   - Who owns what
   - Follow-up survey date

4. ANALYSIS BEST PRACTICES:
   - Look for patterns across multiple responses
   - Weight feedback by rating (lower ratings = more urgent)
   - Identify contradictions or tensions
   - Connect qualitative comments to quantitative scores
   - Be specific with recommendations (actionable, not vague)
   - Include cost/effort estimates for recommendations when possible

5. FORMAT REQUIREMENTS:
   - Professional business formatting
   - Use tables, charts, and visual hierarchy
   - Include response excerpts to support claims
   - Maintain confidentiality (use first names only or anonymize)
   - All outputs should reference the source data date

The Skill should confirm file path is correct before reading, and provide helpful errors if CSV structure is unexpected.

​

Source: https://root-tendency-e9a.notion.site/Rick-Mulready-s-5-Mind-Blowing-Use-Cases-of-Claude-Skills-YouTube-Video-Prompts-from-Video-2a9c2aecc297819e96a6f167037c95c0

