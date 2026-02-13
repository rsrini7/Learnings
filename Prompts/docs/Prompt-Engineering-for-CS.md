# Prompt Engineering for Company Secretaries

### Leveraging Generative AI in Corporate Secretarial Practice

*A practical, jurisdiction-grounded guide — India first, with extensions to Singapore, UK, and USA*

---

## Contents

1. [Generative AI and Company Secretarial Practice](#1-generative-ai-and-company-secretarial-practice)
2. [The CS Regulatory Universe at a Glance](#2-the-cs-regulatory-universe-at-a-glance)
3. [Prompt Engineering Guide — Core Framework](#3-prompt-engineering-guide--core-framework)
4. [Breaking It Down: Goal · Context · Expectations · Source](#4-breaking-it-down-goal--context--expectations--source)
5. [Be Creative — Productivity Multipliers for CS Practice](#5-be-creative--productivity-multipliers-for-cs-practice)
6. [Good Practices and Professional Responsibilities](#6-good-practices-and-professional-responsibilities)
7. [India Use Cases — Detailed Prompt Library](#7-india-use-cases--detailed-prompt-library)
   - 7.1 MCA Filings & ROC Compliance
   - 7.2 SEBI Compliance (Listed Companies)
   - 7.3 Board Meetings — Secretarial Standard SS-1
   - 7.4 General Meetings (AGM/EGM) — Secretarial Standard SS-2
   - 7.5 Statutory Registers
   - 7.6 Secretarial Audit (MR-3)
   - 7.7 FEMA & RBI Compliance
   - 7.8 CSR Compliance
   - 7.9 Insider Trading (SEBI PIT Regulations 2015)
   - 7.10 Mergers, Amalgamations & NCLT Filings
   - 7.11 Corporate Governance Advisory
   - 7.12 Shareholder & Stakeholder Communications
   - 7.13 MSME, IBC & Other Regulatory Obligations
   - 7.14 ESG Governance Advisory
8. [Extension to Other Jurisdictions](#8-extension-to-other-jurisdictions)
   - 8.1 Singapore (ACRA / Companies Act Cap. 50)
   - 8.2 United Kingdom (Companies House / Companies Act 2006)
   - 8.3 United States (SEC / State Corporate Laws)
   - 8.4 UAE (DIFC / ADGM)
9. [Copilot Prompt Examples (Microsoft 365)](#9-copilot-prompt-examples-microsoft-365)
10. [Chaining Prompts — Workflow Sequences](#10-chaining-prompts--workflow-sequences)
11. [Glossary of Key Terms](#11-glossary-of-key-terms)
12. [Quick Reference Card](#12-quick-reference-card)

---

## 1. Generative AI and Company Secretarial Practice

Generative AI has great potential as a copilot to enhance Company Secretaries' (CS) efficacy and efficiency, enabling them to focus their attention on complex, higher-value governance and compliance work. Generative AI tools are only as effective as the input they receive. This guide shares good practices for prompt engineering, helping CS professionals achieve better, verifiable results when using this technology.

Early applications of AI in corporate secretarial practice centred around data analytics — searching large volumes of information, tracking compliance deadlines, and managing documents. AI tools automating tasks such as compliance monitoring, due diligence, and document management have become widespread, but many AI tools have so far seen rudimentary use in the profession.

Generative AI offers an unprecedented opportunity to advance innovation in corporate secretarial practice. By automating routine work, generative AI allows Company Secretaries to focus on higher-value contributions — from offering strategic governance advice to building trusted relationships with boards and regulators — where critical thinking, regulatory acumen, and a holistic understanding of the company's needs come into play.

Studies across professional services have shown that generative AI tools can make professionals significantly quicker on tasks and improve accuracy. The Microsoft CELA organisation reported a **32% speed improvement** and **20% accuracy gain** in comparable knowledge work.

### Use Cases for Company Secretaries Using Appropriate AI Tools

**Compliance Filings:** Preparing and reviewing MCA e-forms (MGT-7, AOC-4, DIR-12, CHG-1, SH-7, DPT-3, MSME-1, BEN-2, and others), annual returns, director appointments, share allotments, charge filings.

**SEBI Compliance:** Drafting and reviewing disclosures under LODR Regulations 2015 (Regulations 13, 23, 30, 33, 34, 36, 40, 46), insider trading compliance, SAST obligations.

**Governance Advisory:** Researching and summarising corporate governance norms — board composition, committee charters, related party transaction policies — under ICSI guidelines, SEBI LODR, and the Companies Act 2013.

**Meeting Management:** Drafting notices, agendas, and minutes for board and shareholder meetings in compliance with Secretarial Standards SS-1 and SS-2.

**Statutory Registers:** Generating summaries, reconciliations, and updates for registers of members, directors, beneficial ownership, charges, and related-party contracts.

**Secretarial Audit:** Assisting in MR-3 secretarial audit reports, compliance certificates, and generating multi-law checklists.

**FEMA & RBI Compliance:** Drafting filings for foreign investment (FC-GPR, FC-TRS, FCTRS), ECB reporting, ODI filings, and compounding applications.

**Risk Assessment:** Identifying governance risks in mergers, acquisitions, joint ventures, and cross-border transactions.

**Shareholder Communications:** Drafting notices, explanatory statements under Section 102, postal ballot notices, and investor grievance responses.

**NCLT / IBC Work:** Supporting petition drafting, scheme of arrangement documents, and IBC-related compliance checklists.

**Practice Management:** Generating compliance trackers, calendars, fee narratives, and audit trail reports.

---

## 2. The CS Regulatory Universe at a Glance

Understanding the regulatory landscape is essential for writing accurate, targeted prompts. The table below maps the core laws, regulators, and instruments a CS in India works with.

| Domain | Primary Law / Regulation | Regulator / Authority | Key Forms / Instruments |
|---|---|---|---|
| Company incorporation & governance | Companies Act 2013 | MCA / RoC / NCLT | SPICe+, INC-22, DIR-12, MGT-7, AOC-4 |
| Securities (listed cos.) | SEBI (LODR) Regs 2015 | SEBI / Stock Exchanges (BSE/NSE) | Reg. 30 disclosures, Reg. 33 results, Reg. 46 website |
| Capital raising | SEBI (ICDR) Regs 2018 | SEBI | Prospectus, Letter of Offer, AoA amendments |
| Insider trading | SEBI (PIT) Regs 2015 | SEBI | Pre-clearance forms, UPSI register, trading windows |
| Substantial acquisition | SEBI (SAST) Regs 2011 | SEBI | Reg. 29/30/31 disclosures |
| Secretarial Standards | SS-1 (Board), SS-2 (General meetings) | ICSI | Meeting notices, minutes templates |
| Foreign exchange | FEMA 1999 + RBI Master Directions | RBI / AD Banks | FC-GPR, FC-TRS, FCTRS, FCGPR, ODI-Part I/II |
| Foreign investment | FEMA (Non-Debt Instruments) Rules 2019 | RBI / DPIIT | FIFP portal filings |
| Charges | Companies Act 2013, Sections 77–87 | MCA / RoC | CHG-1, CHG-4, CHG-9 |
| Beneficial ownership | Section 90 of Companies Act | MCA | BEN-1, BEN-2 |
| MSME vendor dues | MSMED Act 2006 | MCA | MSME-1 (half-yearly) |
| Deposits | Companies Act 2013, Chapter V | MCA | DPT-3 |
| Secretarial audit | Section 204, Companies Act 2013 | ICSI | MR-3 Report |
| CSR | Section 135 + CSR Rules 2014 | MCA | Annual CSR Report, CSR-2 |
| Insolvency | IBC 2016 | NCLT / IBBI | Section 7/9/10 applications |
| Mergers / schemes | Sections 230–232, Companies Act | NCLT | NCLT scheme petitions |
| Labour (retrenchment) | Industrial Disputes Act 1947 | Labour authorities | Form Q, intimation letters |

---

## 3. Prompt Engineering Guide — Core Framework

Knowing the basics of prompt engineering — the practice of formulating instructions to achieve specific outcomes from a generative AI tool — enables Company Secretaries to generate more accurate and pertinent results. This section provides concepts applicable to most prompt-based generative AI tools, including Claude, ChatGPT, Microsoft Copilot, and specialised compliance platforms.

With prompt-based generative AI, the user interacts with the model by entering a text prompt, to which the model responds with a text completion or output. While these AI models are powerful, their behaviour is very sensitive to the prompt. This makes prompt engineering an important skill to develop.

In practice, the prompts guide the AI model to complete the desired task. It is more of an art than a science, often requiring experience and intuition to craft a successful prompt.

### The Four-Part Prompt Structure

A good prompt for CS work provides a **clear description of the task**, explains the **role the AI tool needs to play**, describes the **audience**, provides **guidance on tone, style, and format**, and provides **reference material or law**. An iterative process will always refine results.

```
| GOAL | CONTEXT | EXPECTATIONS | SOURCE |
|------|----------|--------------|---------|
| What do you want from the AI system? | Why do you need it and who is involved? | How should the AI best respond? | What reference material should the system use? |
| "Draft a notice of AGM..." | "...for an AGM of a listed company in India..." | "Respond in formal legal language, include explanatory statement..." | "...base it on SS-2 of ICSI and Sec. 101 of Companies Act 2013." |
```

**Full example built from the framework:**

> *"Draft a notice of Annual General Meeting for a listed public company incorporated under the Companies Act 2013. I am the Company Secretary advising the board. The meeting is to be held via VC/OAVM mode. Include all mandatory agenda items — adoption of accounts, declaration of dividend, re-appointment of retiring directors (Section 152), and ratification of statutory auditors (if applicable). Attach an explanatory statement under Section 102 for all special business. Respond in formal legal language appropriate for dispatch to shareholders. Base the notice on Secretarial Standard-2 (SS-2) issued by ICSI, Section 101 of the Companies Act 2013, and MCA Circular No. 14/2020 on virtual meetings."*

---

## 4. Breaking It Down: Goal · Context · Expectations · Source

### 4.1 Goal

Start with clear instructions by laying out your goal at the very beginning of the prompt. The sequence that information appears matters — telling the model the task before sharing context produces higher quality output.

- Provide clear objectives — filing review, draft creation, compliance check, gap analysis
- Use action verbs: **"Draft"**, **"Analyse"**, **"Summarise"**, **"Identify"**, **"Generate"**, **"Review"**, **"Compare"**, **"Extract"**
- If goals are complex, break them down: "First identify all gaps. Then generate a correction table. Then draft the rectified form."

### 4.2 Context

Include relevant background, constraints, and parties involved. For CS work, context almost always includes:

- **Persona**: "I am a Company Secretary / Practising CS / In-house CS of a listed entity"
- **Company type**: Private limited, public limited, listed, OPC, Section 8, NBFC, foreign subsidiary
- **Jurisdiction**: India / Singapore / UK / USA / UAE
- **Applicable law**: Companies Act 2013, SEBI LODR, FEMA, etc.
- **Applicable Secretarial Standard**: SS-1 for board meetings, SS-2 for general meetings
- **Audience of output**: Board of Directors, RoC, SEBI, shareholders, stock exchange, auditors
- **Few-shot examples**: Paste sample clauses, previous resolutions, or templates for the AI to emulate

### 4.3 Expectations

Set how the output should be framed:

- **Format**: Table (with column headings), checklist, resolution text, notice, draft e-form, narrative report
- **Tone**: Formal legal language, authoritative, plain English for shareholders
- **Depth**: High-level summary vs. granular clause-by-clause analysis
- **Chain-of-Thought**: For complex compliance tasks, add "Think step-by-step" — this causes the model to reason through each issue before producing the output
- **Length or limits**: "Respond in no more than 500 words" or "produce a table — one row per compliance item"
- **Citations**: "Cite specific section numbers and regulation numbers in the output"

### 4.4 Source

For CS work, precision in source material dramatically improves output quality.

- Upload or paste relevant documents: draft resolutions, existing minutes, MCA form XML, charge certificates, loan agreements
- Reference specific sections: "Section 149(6) of the Companies Act 2013" rather than "director appointment rules"
- Reference specific ICSI Secretarial Standards: "Clause 1.3.2 of SS-1"
- Reference specific SEBI regulation numbers: "Regulation 23(9) of SEBI LODR Regulations 2015"
- Reference official portals: MCA21 portal guidelines, SEBI SCORES portal, NSE/BSE Listing Centre documentation
- Always anonymise / redact client-specific confidential information before pasting into a general-purpose AI tool

> **⚠ Important:** Always verify AI-generated output against the source law before use. The AI may confuse section numbers across amendments or between jurisdictions. Do not file or dispatch any AI-generated document without independent review.

---

## 5. Be Creative — Productivity Multipliers for CS Practice

Properly crafted prompts can dramatically boost productivity and creativity for Company Secretaries. Here are key areas where generative AI adds practical value:

**Generate Content Ideas** — Redraft board resolutions or compliance checklists. Overcome writer's block on explanatory statements or CSR policy narrative. Generate alternative phrasings for sensitive disclosures.

**Enable Insightful Meetings** — Summarise recorded/transcribed board calls, convert rough meeting notes into structured minutes, extract action items with owner names and deadlines from meeting transcripts.

**Assist with Storytelling** — Convert dry governance compliance summaries into readable Board Reports, Corporate Governance Reports, or Integrated Annual Report sections.

**Gain Insights** — Summarise lengthy regulations (Companies Act amendments, SEBI consultation papers, MCA notification circulars) and ask follow-up questions to probe specific provisions.

**Translation** — Translate foreign subsidiary regulations, foreign contracts, or FATF / OECD guidelines from other languages for multinational compliance work.

**Expand on Key Points** — Convert bullet-point compliance gaps identified during audit into a full draft letter to the board, or into a board presentation with risk ratings.

**Compliance Calendar Drafting** — Convert a statutory compliance matrix into a month-wise action calendar with form names, deadlines, and responsible owners.

**Drafting Training Material** — Create plain-language summaries of SEBI regulations or Companies Act provisions for training Directors, Key Managerial Personnel, or new team members.

---

## 6. Good Practices and Professional Responsibilities

Generative AI enhances efficiency but must align with the professional and ethical responsibilities of a Practising Company Secretary (PCS) or In-House CS.

**Professionalism.** You are responsible for every document you sign, certify, or file, even when you used generative AI to draft it. Section 448 of the Companies Act 2013 (false statements in documents) and ICSI disciplinary proceedings apply to you — not to the AI. Review and verify every output before use.

**Copilot, not Autopilot.** Generative AI works best when you provide substantive content and context. A CS's craft is in governance advisory, regulatory interpretation, and professional certification. AI is helpful for drafting and synthesis but must not substitute for developing subject-matter expertise or professional judgement.

**Disclosure.** Be aware of your firm's policy and applicable professional guidance on disclosure of AI use. ICSI guidelines on professional responsibility continue to apply.

**Confidentiality.** Free-to-use generative AI services may use prompt content for model training. Before using any general-purpose tool, anonymise your prompts by replacing company names, CIN numbers, director names, and financial figures with placeholders. Use enterprise-grade tools with robust data protection agreements for sensitive work.

**Verification.** Never file an MCA e-form, SEBI disclosure, or statutory document based solely on AI output. Cross-check section numbers, form names, deadlines, and thresholds against the primary source — MCA portal, SEBI website, or ICSI compendium.

| **DO** | **DON'T** |
|---|---|
| Use AI for comparisons, summaries, first drafts, and brainstorming based on trusted regulatory sources | Overload a single prompt with multiple complex tasks — break them into a chain |
| Start a new chat for each distinct task; provide fresh, clear context every time | Expect perfect output on a single try — iterate |
| Chain prompts logically: analyse → identify gaps → draft correction → verify → generate filing checklist | Assume AI output is legally accurate or up to date with the latest amendments |
| Specify the exact law, section, and secretarial standard in every prompt | File or dispatch AI-generated documents without independent professional review |
| Experiment, iterate, and save your best prompt templates | Share actual client CIN, PAN, DPIN, financial data with non-enterprise AI tools |
| Request citations and cross-references in the output for easy verification | Rely on AI to determine whether a transaction requires regulatory approval |

---

## 7. India Use Cases — Detailed Prompt Library

> **Quick Tip:** Many prompts for CS work require reference to documents. Upload or paste the relevant document (annual return draft, charge document, meeting transcript) into the AI tool's prompt window. Always redact sensitive client identifiers first.

---

### 7.1 MCA Filings & ROC Compliance

**Use Case: Review Annual Return Draft (MGT-7 / MGT-7A)**

> *"Analyse the attached draft Annual Return (Form MGT-7) for a listed public company. I am a Practising Company Secretary conducting a compliance review under Section 92 of the Companies Act 2013. Identify any gaps, inaccuracies, or missing disclosures. Present findings in a table with the following columns: Item Number | Form Field / Annexure | Section / Rule Reference | Description of Issue | Suggested Correction. Base the review on the Companies (Management and Administration) Rules 2014 and MCA's MGT-7 e-form instructions."*

---

**Use Case: Director Appointment — DIR-12 Pre-Filing Checklist**

> *"Generate a step-by-step pre-filing checklist for submitting Form DIR-12 on the MCA21 portal for the appointment of an Additional Director under Section 161(1) of the Companies Act 2013. I am the Company Secretary of a private limited company. The checklist should cover: DIN verification, consent letter (DIR-2), intimation to MCA within 30 days, board resolution requirement, attachments required, and filing fee. Format as a numbered checklist with the applicable rule or section next to each step."*

---

**Use Case: Charge Registration — CHG-1**

> *"Draft a compliance action plan for registering a charge created by a term loan agreement under Section 77 of the Companies Act 2013. I am the Company Secretary of the borrower company. The charge was created on [DATE]. Outline: (1) the 30-day filing window and extended 60-day condonation window under Section 77(1), (2) required attachments for Form CHG-1, (3) consequences of non-registration under Section 77(3), and (4) verification items before submission. Present in a numbered action list citing relevant sections and the Companies (Registration of Charges) Rules 2014."*

---

**Use Case: Board Resolution — MGT-14 Filing**

> *"Identify which types of board resolutions passed at a board meeting of a public company require filing with the RoC through Form MGT-14 under Section 117 of the Companies Act 2013. Present in a table: Resolution Type | Section / Provision | Filing Deadline | Attachment Required. Focus on resolutions under Sections 179(3), 180, 186, and 188, and any other matters listed in Rule 24 of the Companies (Management and Administration) Rules 2014."*

---

**Use Case: Return of Deposits — DPT-3**

> *"Draft a compliance note for the Board on the requirement to file Form DPT-3 (Return of Deposits) under Rule 16 of the Companies (Acceptance of Deposits) Rules 2014. I am the Company Secretary of a private company that has outstanding borrowings from directors. Cover: (a) whether director loans fall within 'deposits' definition after the 2019 amendment to the Deposits Rules, (b) the annual filing deadline (30 June), (c) required attachments — auditor's certificate, and (d) penal consequences under Section 76A for non-filing. Cite the relevant sections and rules throughout."*

---

**Use Case: Beneficial Ownership — Section 90 / BEN-2**

> *"Generate a compliance checklist for maintaining significant beneficial ownership (SBO) records under Section 90 of the Companies Act 2013 and the Companies (Significant Beneficial Owners) Rules 2018. I am a Company Secretary of a company with a complex shareholding structure involving corporate shareholders. The checklist should cover: (1) identifying SBOs (25% threshold for voting rights / shareholding), (2) issuing notice in Form BEN-4, (3) receiving declarations in Form BEN-1, (4) filing Form BEN-2 with RoC, and (5) maintaining the Register of SBOs. Include deadlines and section references."*

---

### 7.2 SEBI Compliance (Listed Companies)

**Use Case: SEBI LODR Compliance Calendar — Listed Company**

> *"Generate a month-wise annual compliance calendar for a BSE/NSE-listed public company under the SEBI (Listing Obligations and Disclosure Requirements) Regulations 2015. I am the Company Secretary of the listed entity. The calendar should cover Regulations 7, 13, 17-27 (corporate governance), 29, 30, 33, 34, 36, 40, 44, 46, and 47 across each quarter. Format the calendar as a table: Month | Compliance Obligation | Regulation Number | Deadline | Responsible Department | Filing Platform (BSE/NSE/SEBI SCORES). Distinguish between quarterly, half-yearly, and annual obligations."*

---

**Use Case: Material Event Disclosure — Regulation 30**

> *"Draft a disclosure to the stock exchange under Regulation 30 of the SEBI LODR Regulations 2015 for the following material event: [describe event — e.g., resignation of Managing Director, signing of a major contract, outcome of NCLT proceedings]. I am the Company Secretary. The disclosure must be made within 24 hours of the board decision (or within 30 minutes for outcomes of board meetings). Use the prescribed disclosure format and include: nature of the event, brief details, impact on the company, and whether there are any legal/financial implications. Keep the language factual, formal, and precise."*

---

**Use Case: Related Party Transaction — Regulation 23**

> *"Analyse the following related party transaction proposal for compliance with Regulation 23 of the SEBI LODR Regulations 2015 and Section 188 of the Companies Act 2013. I am the Company Secretary advising the Audit Committee. The proposed transaction involves [description of transaction] between the company and [related party name/relationship]. Think step-by-step and assess: (1) whether the transaction meets the 'material RPT' threshold under Reg. 23(1) (10% of consolidated turnover), (2) whether shareholder approval is required, (3) whether Audit Committee prior approval is needed, (4) disclosure obligations on stock exchanges, and (5) required disclosures in the Annual Report. Cite all applicable regulations and sections."*

---

**Use Case: Corporate Governance Report — Regulation 34 / Schedule V**

> *"Draft the Corporate Governance Report section for inclusion in the Annual Report of a listed company, as required under Regulation 34(3) read with Schedule V Part C of the SEBI LODR Regulations 2015. I am the Company Secretary. The report should include: (1) company's philosophy on Corporate Governance, (2) Board composition table (category, DIN, attendance, committee memberships), (3) Audit Committee details, (4) Nomination and Remuneration Committee details, (5) Stakeholders' Relationship Committee details, (6) general body meeting details for the last 3 years, (7) means of communication, and (8) general shareholder information. Use formal language appropriate for an Annual Report. Indicate where I need to insert actual data."*

---

**Use Case: Quarterly Compliance Report — Regulation 27(2)**

> *"Generate a draft quarterly compliance report under Regulation 27(2) of the SEBI LODR Regulations 2015 for submission to the stock exchange. I am the Company Secretary. The report covers the quarter ended [DATE]. Include the standard annexure format confirming compliance / non-compliance (with reasons) for: Board composition (Reg. 17), Audit Committee (Reg. 18), NRC (Reg. 19), Stakeholders' RC (Reg. 20), Risk Management Committee (Reg. 21), Related Party transactions policy (Reg. 23), and CEO/CFO certification (Reg. 17(8)). Format as the prescribed annexure table."*

---

### 7.3 Board Meetings — Secretarial Standard SS-1

**Use Case: Notice and Agenda for Board Meeting**

> *"Draft a formal notice convening a Board Meeting of [Company Type] under Clause 1.3.2 of Secretarial Standard-1 (SS-1) issued by ICSI, read with Section 173(3) of the Companies Act 2013. I am the Company Secretary. The meeting is to be held via Video Conferencing (VC). Notice must be sent at least 7 days in advance (unless shorter notice is consented to). The agenda items are: (1) adoption of unaudited quarterly financial results under Regulation 33 SEBI LODR (for listed company), (2) approval of related party transactions under Section 188, (3) grant of loan to subsidiary under Section 186(3), (4) any other business with leave of the Chair. Format the notice and agenda in separate sections. Include all mandatory SS-1 disclosures: quorum requirements, facility for VC participation, and director conflict of interest declaration requirement."*

---

**Use Case: Board Meeting Minutes — Drafting**

> *"Draft board meeting minutes based on the following rough notes [paste notes]. I am the Company Secretary. The minutes should comply with Clause 7 of Secretarial Standard-1 (SS-1) issued by ICSI. Ensure the minutes: (1) record the names of directors present in person and via VC and those who sent apologies, (2) record the quorum present and who chaired the meeting, (3) summarise discussions on each agenda item without verbatim reproduction, (4) clearly state each resolution passed (ordinary or special) with voting outcome, (5) note any conflict of interest declarations under Section 184, and (6) end with confirmation of the next meeting date. Use formal, third-person language. Do not fabricate any information not present in the notes."*

---

**Use Case: Director Conflict of Interest — Section 184 Compliance Check**

> *"Generate a checklist for Company Secretaries to manage director conflict of interest disclosures under Section 184(1) and 184(2) of the Companies Act 2013 and Clause 4 of Secretarial Standard-1 (SS-1). Cover: (1) maintaining Form MBP-1 (Notice of Interest by Director), (2) updating MBP-1 upon change in interest at first board meeting of each financial year, (3) restricting interested directors from voting under Section 184(2), (4) recording disclosure and abstention in minutes, and (5) maintenance of Register of Contracts under Section 189. Present as a step-by-step compliance protocol."*

---

### 7.4 General Meetings (AGM/EGM) — Secretarial Standard SS-2

**Use Case: AGM Notice and Explanatory Statement**

> *"Draft a Notice of Annual General Meeting for a listed public company under Section 101 of the Companies Act 2013, Rule 18 of the Companies (Management and Administration) Rules 2014, and Secretarial Standard-2 (SS-2) issued by ICSI. I am the Company Secretary. The AGM is to be held through VC/OAVM mode per MCA General Circular No. 10/2022. Ordinary business items: adoption of financial statements (standalone + consolidated), declaration of final dividend, re-appointment of Director retiring by rotation (Section 152(6)), ratification of auditors (if applicable). Special business: appointment of Independent Director, increase in authorised share capital (Section 61), and approval of material RPT. Include: (1) detailed explanatory statement under Section 102 for all special business, (2) notes on attendance via VC, e-voting, and IEPF, (3) route map if meeting has physical venue, (4) Proxy Form (Section 105) for physical meetings, and (5) attendance slip. Indicate placeholders for actual data. Use formal language."*

---

**Use Case: Postal Ballot — Section 110**

> *"Draft a complete postal ballot notice under Section 110 of the Companies Act 2013 and the Companies (Management and Administration) Rules 2014 (Rule 22) for passing a special resolution to alter the Object Clause of the Memorandum of Association under Section 13. I am the Company Secretary. The notice must: (1) specify the proposed alteration to Clause III of the MoA, (2) include an explanatory statement per Section 102 with detailed rationale, (3) appoint a Scrutiniser from a list of Practising CS / CA, (4) specify the remote e-voting window (minimum 30 days from dispatch), (5) state the NSDL/CDSL e-voting portal and login instructions, and (6) include the draft resolution. Format as a formal, dispatch-ready notice."*

---

**Use Case: Shareholder Meeting — Quorum and Adjournment Rules**

> *"Summarise the quorum requirements for Annual General Meetings and Extraordinary General Meetings of public and private companies under Section 103 of the Companies Act 2013 and Clause 5 of Secretarial Standard-2 (SS-2). Then explain the procedure for adjournment of a general meeting under Section 103(2) if quorum is not present within 30 minutes of the scheduled time. Finally, outline the notice requirements for adjourned meetings. Present in three clearly labelled sections. Cite section numbers and SS-2 clause references throughout."*

---

### 7.5 Statutory Registers

**Use Case: Register of Members Post Share Transfer — Section 88**

> *"Generate a step-by-step checklist for updating the Register of Members under Section 88 of the Companies Act 2013 following a share transfer by a shareholder. I am the Company Secretary of a private limited company. The transfer is a private off-market transfer. The checklist should cover: (1) receiving and verifying the Share Transfer Form (SH-4) under Section 56(1), (2) verifying share certificates, (3) board approval for registration of transfer within 30 days (Section 56(4)), (4) issuance of new share certificate under Section 56(1) within 1 month of lodgement, (5) updating the Register of Members (folio, name, address, shares held, date of entry), (6) filing Form SH-7 if share capital structure changes, and (7) retention of old share certificates. Include section and rule references."*

---

**Use Case: Register of Contracts — Section 189**

> *"Draft a template for maintaining the Register of Contracts or Arrangements in which Directors are Interested under Section 189 of the Companies Act 2013 and Rule 16 of the Companies (Meetings of Board and its Powers) Rules 2014. I am the Company Secretary. The register must contain: name of company / firm / party to the contract, nature of relationship, nature/value of contract, date of board approval, and name of directors interested. Format as a register table with appropriate column headings. Include a note on the obligation of directors to disclose interests at the beginning of each financial year under Section 184(1)."*

---

### 7.6 Secretarial Audit (MR-3)

**Use Case: Secretarial Audit Checklist — Multi-Law Compliance**

> *"Generate a comprehensive checklist for conducting a Secretarial Audit under Section 204 of the Companies Act 2013 for a listed public company for the financial year [YEAR]. I am a Practising Company Secretary. The audit must cover compliance with: (1) Companies Act 2013 and rules thereunder, (2) SEBI Act 1992 and SEBI LODR Regulations 2015, (3) SEBI (PIT) Regulations 2015, (4) SEBI (SAST) Regulations 2011, (5) FEMA 1999 (to the extent of FDI / ECB), (6) Secretarial Standards SS-1 and SS-2. For each law, list the 5 most critical compliance checkpoints. Format as a table: Law / Regulation | Compliance Item | Section / Reg. Number | Verification Method | Status (Complied / Non-Complied / N/A)."*

---

**Use Case: MR-3 Report Qualification Drafting**

> *"Draft a qualification paragraph for inclusion in a Secretarial Audit Report (Form MR-3) under Section 204 of the Companies Act 2013. The audit has revealed the following non-compliance: the company failed to file Form MGT-14 within 30 days of passing a board resolution approving a loan to a related party under Section 186(3), as required by Section 117(3)(g) of the Companies Act 2013. The delay was [X] days. Draft the qualification in formal, professional language appropriate for an MR-3 report, including: (1) description of the non-compliance, (2) section/regulation reference, (3) period of non-compliance, and (4) management's explanation if any. Do not include any financial penalty amount as this must be verified independently."*

---

### 7.7 FEMA & RBI Compliance

**Use Case: FC-GPR Filing Checklist — FDI Reporting**

> *"Generate a step-by-step compliance checklist for reporting foreign direct investment (FDI) received by an Indian company through Form FC-GPR on the RBI's FIRMS portal. I am the Company Secretary. The FDI has been received from a foreign investor in a fresh equity allotment. The checklist must cover: (1) KYC and FIRC/FIRA receipt from the AD Bank, (2) valuation certificate requirement (DCF / Fair Value from a CA / SEBI-registered Merchant Banker), (3) timeline for reporting — within 30 days of allotment per Para 4 of Schedule I to FEMA (NDI) Rules 2019, (4) upload of board resolution for allotment, Form FC-GPR on FIRMS portal (Entity Master and Investment Entry), and (5) consequences of delayed reporting / compounding under FEMA 1999 Section 15. Cite the applicable FEMA provision and RBI Master Direction for each step."*

---

**Use Case: Transfer of Shares to Non-Resident — FC-TRS**

> *"Summarise the compliance requirements for reporting transfer of shares from a resident to a non-resident under Form FC-TRS as per Para 9 of Schedule I to the Foreign Exchange Management (Non-Debt Instruments) Rules 2019 and the RBI Master Direction on Reporting. I am the Company Secretary. Cover: (1) parties responsible for filing (transferee in case of sale to NR), (2) 60-day deadline from receipt of remittance, (3) required documents (share transfer form SH-4, valuation certificate, FIRC), (4) filing on the FIRMS portal, and (5) price discovery guidelines (no below-fair-value sale to NR). Present in a numbered, step-by-step format with RBI directive references."*

---

### 7.8 CSR Compliance

**Use Case: CSR Compliance Note — Section 135**

> *"Draft a comprehensive compliance note for the Board of Directors on Corporate Social Responsibility (CSR) obligations under Section 135 of the Companies Act 2013 and the Companies (CSR Policy) Rules 2014 (as amended in 2021). I am the Company Secretary. The company has a net worth of ₹500 crore+ / turnover of ₹1,000 crore+ / net profit of ₹5 crore+. Cover: (1) applicability thresholds (Section 135(1)), (2) composition of CSR Committee (Section 135(1) — at least 3 directors including 1 Independent Director), (3) calculation of 2% CSR spending obligation (average net profits of last 3 years under Section 135(5)), (4) permissible CSR activities (Schedule VII), (5) obligations under Rule 5 for unspent amounts — transfer to Schedule VII activity or PM CARES within 30 days of FY end, or into Unspent CSR Account within 30 days and spending within 3 years, (6) Form CSR-2 annual filing requirements, and (7) disclosure in Board Report under Section 134(3)(o). Cite applicable sections and rules throughout."*

---

### 7.9 Insider Trading (SEBI PIT Regulations 2015)

**Use Case: Insider Trading Compliance Framework**

> *"Draft a board note summarising the compliance framework for prevention of insider trading under the SEBI (Prohibition of Insider Trading) Regulations 2015 (as amended). I am the Company Secretary of a listed company acting as the Compliance Officer under Regulation 2(1)(c). The note should cover: (1) definition of 'insider' and 'UPSI' under Regulations 2(1)(g) and 2(1)(n), (2) trading window closure policy under Schedule B — closure during 48 hours before and after UPSI becoming generally available, (3) pre-clearance requirements under Schedule B for trades above threshold by designated persons (Regulation 9), (4) maintenance of a Structured Digital Database (SDD) under Regulation 3(5) — third-party sharing of UPSI, (5) Code of Conduct obligations under Schedule A and B, (6) annual disclosure requirements under Regulation 7 — initial, continual, and annual disclosures, and (7) obligations on the company to report suspected insider trading. Format as a structured board note with numbered sections."*

---

**Use Case: Trading Window Intimation to Designated Persons**

> *"Draft a trading window closure notice to be sent to all Designated Persons of a listed company under the SEBI (PIT) Regulations 2015 and the company's Code of Conduct. I am the Company Secretary. The trading window is being closed from [DATE] in connection with the upcoming board meeting for approval of quarterly/annual financial results under Regulation 33 SEBI LODR. The notice should: (1) state the date from which the window is closed, (2) state that trading in company securities is prohibited during this period, (3) remind designated persons of pre-clearance requirements for any transactions, (4) state the UPSI that is the basis for closure (without specifying the financial outcome), and (5) advise on re-opening after 48 hours following public dissemination of results. Use formal, concise language."*

---

### 7.10 Mergers, Amalgamations & NCLT Filings

**Use Case: Scheme of Arrangement — Compliance Roadmap**

> *"Generate a step-by-step compliance roadmap for implementing a merger of two wholly owned subsidiaries into the holding company (forward merger) under Sections 230–232 of the Companies Act 2013. I am the Company Secretary of the holding company (Transferee Company). The roadmap should cover all stages from planning to effective date: (1) Board approval of the scheme (Section 230(1)) and filing Form CAA-1 (NCLT application), (2) notice to RoC, RD, Income Tax, SEBI (for listed companies), Competition Commission of India (if thresholds triggered), and other regulators, (3) NCLT's First Motion Order — meeting directions, (4) dispatch of Notice to shareholders and creditors for meeting / dispensation application, (5) conduct of Court Convened Meeting, (6) filing of scheme documents with stock exchanges (SEBI Circular SEBI/HO/CFD/DIL3/CIR/P/2021/0000000666 for listed companies), (7) NCLT Second Motion — approval hearing, (8) filing of NCLT Order with RoC in Form INC-28, and (9) effective date and consequential steps (share allotment, asset transfer, register updates). Format as a numbered timeline. Cite applicable sections for each step."*

---

**Use Case: NCLT Petition — Oppression and Mismanagement**

> *"Summarise the legal grounds and procedural steps for filing a petition under Section 241 read with Section 242 of the Companies Act 2013 before the National Company Law Tribunal (NCLT) for relief from oppression and mismanagement. I am advising the minority shareholders holding [X]% of the company. Cover: (1) locus standi requirements under Section 244(1) — minimum 100 members or 10% of total number of members, or holders of 10% paid-up share capital (for non-personal), (2) grounds constituting 'oppression' and 'mismanagement', (3) reliefs available under Section 242 (winding up on just and equitable grounds, purchase of shares, management change), (4) interim relief application, and (5) appeal to NCLAT under Section 421. Indicate which documents are typically required and cite relevant sections."*

---

### 7.11 Corporate Governance Advisory

**Use Case: Board Composition — Independent Director Requirements**

> *"Analyse the board composition requirements for a listed public company under Section 149 of the Companies Act 2013 and Regulation 17 of the SEBI LODR Regulations 2015. I am the Company Secretary advising the Nomination and Remuneration Committee. Cover: (1) minimum number of independent directors (Section 149(4) — at least 1/3 of total board), (2) enhanced requirement under Regulation 17(1)(b) — at least half the board to be independent if Chairperson is Executive or belongs to promoter group, (3) definition of independence under Section 149(6) and Regulation 16(1)(b), (4) tenure limits — 5 + 5 years with a cooling-off period (Section 149(10-11)), (5) Data Bank of Independent Directors on MCA portal requirement under Rule 6 of Companies (Appointment and Qualification of Directors) Rules 2014, (6) annual declaration of independence (Section 149(7)), and (7) peer review and performance evaluation under Schedule IV (Code for Independent Directors). Present as a structured governance advisory note with section references."*

---

**Use Case: Nomination and Remuneration Policy — Section 178**

> *"Draft an outline for a Nomination and Remuneration Policy as required under Section 178(3) of the Companies Act 2013 and Regulation 19(4) read with Part D of Schedule II to the SEBI LODR Regulations 2015. I am the Company Secretary. The policy should cover: (1) criteria for determining qualifications, positive attributes, and independence of a director, (2) remuneration policy for directors, KMPs, and senior management — linking pay to performance, (3) board diversity policy, (4) tenure and succession planning, and (5) evaluation criteria. Draft section headings and a summary of content for each section, in formal language suitable for board adoption."*

---

### 7.12 Shareholder & Stakeholder Communications

**Use Case: Investor Grievance Response — SEBI SCORES**

> *"Draft a formal response to a shareholder complaint registered on the SEBI SCORES platform. I am the Company Secretary. The complaint relates to non-receipt of dividend declared at the AGM held on [DATE]. The response should: (1) acknowledge receipt of the complaint and SCORES reference number, (2) confirm the dividend amount declared and record date, (3) explain the process for re-issuance or NEFT credit if the bank mandate was not updated, (4) request the shareholder to update bank mandate with the Registrar and Share Transfer Agent (RTA), (5) provide RTA contact details, and (6) confirm resolution timeline within 30 days per SEBI guidelines. Use formal, empathetic language. Do not include any information beyond what I have provided."*

---

**Use Case: Annual Report — Directors' Report Checklist**

> *"Generate a comprehensive checklist of mandatory disclosures required in the Board's Report (Directors' Report) of a listed public company for a financial year ending 31 March [YEAR], under Section 134 of the Companies Act 2013. I am the Company Secretary. For each disclosure requirement, specify: Item | Section / Rule / Regulation | Whether Mandatory for Listed Co | Notes. Cover at minimum: extract of annual return (MGT-9 / web-link post 2020 amendment), number of board meetings, Directors' Responsibility Statement (Section 134(5)), Secretarial Audit Report (MR-3), CSR Report, NRC policy, energy conservation (Rule 8(3)(A)), foreign exchange (Rule 8(3)(B)), R&D, conservation measures, ESOP disclosures, risk management statement, internal financial controls (Section 134(5)(e)), loans/investments/guarantees (Section 186), RPT disclosures (Section 188), IEPF transfers (Section 125), dividend policy, and corporate governance report per SEBI LODR."*

---

### 7.13 MSME, IBC & Other Regulatory Obligations

**Use Case: MSME-1 Half-Yearly Filing**

> *"Summarise the compliance requirements for Form MSME-1 (Half-Yearly Return on Outstanding Dues to Micro and Small Enterprises) under Section 405 of the Companies Act 2013 read with the Specified Companies (Furnishing of Information about Payment to Micro and Small Enterprises Suppliers) Order 2019. I am the Company Secretary. Cover: (1) which companies must file (all companies that receive supplies from MSMEs), (2) the two half-yearly filing periods (April–September: by 31 October; October–March: by 30 April), (3) what to disclose — name of MSME supplier, amount outstanding, and number of days outstanding, (4) verification steps before filing (supplier MSME registration status), and (5) penalty for non-compliance under Section 405(4). Format as a numbered compliance protocol."*

---

**Use Case: IBC Creditor — Section 7 Application Checklist**

> *"Generate a checklist of documents and procedural steps required for a financial creditor to file an application under Section 7 of the Insolvency and Bankruptcy Code 2016 before the National Company Law Tribunal (NCLT) for initiation of Corporate Insolvency Resolution Process (CIRP) against a corporate debtor. I am advising the in-house legal and secretarial team of the creditor company. The checklist should cover: (1) Form 1 (application format under IBC Rules 2016), (2) proof of financial debt (loan agreement, sanction letter, statement of account), (3) proof of default (CIBIL / credit bureau record, demand notice record), (4) filing fee, (5) IRP nomination (if any), (6) limitation period — 3 years from date of default (Limitation Act), and (7) NCLT registry requirements. Cite the IBC section and CIRP Regulations reference for each item."*

---

### 7.14 ESG Governance Advisory

ESG (Environmental, Social, and Governance) advisory is a rapidly growing area of responsibility for Company Secretaries, particularly for listed entities required to publish a Business Responsibility and Sustainability Report (BRSR) under Regulation 34(2)(f) of the SEBI LODR Regulations 2015. Alongside CSR obligations under Section 135 of the Companies Act 2013, ESG now cuts across statutory filings, board advisory, risk management, and investor disclosures. The prompts below help CS professionals assess ESG compliance, draft frameworks, prepare disclosures, and integrate sustainability considerations into governance.

**Regulatory Anchors for ESG in India:**
- SEBI LODR Regulation 34(2)(f) — BRSR mandatory for top 1,000 listed entities (by market cap) from FY 2022-23; BRSR Core with reasonable assurance from FY 2024-25
- SEBI Circular SEBI/HO/CFD/CMD-2/P/CIR/2021/562 — BRSR format and guidance
- National Guidelines on Responsible Business Conduct (NGRBC) — 9 Principles issued by MCA
- Section 135, Companies Act 2013 + CSR Rules 2014 (as amended 2021) — Social dimension
- Environment Protection Act 1986 + Water/Air (Prevention & Control of Pollution) Acts — Environmental dimension
- Prevention of Corruption Act 1988 — Governance / Anti-bribery dimension
- SEBI (LODR) Regulation 4(2)(f)(ii)(9) — Board oversight of sustainability / ESG

---

**Use Case: BRSR Compliance Checklist — SEBI Regulation 34(2)(f)**

> *"Generate a compliance checklist for preparing the Business Responsibility and Sustainability Report (BRSR) under Regulation 34(2)(f) of the SEBI LODR Regulations 2015 for a listed public company in the top 1,000 by market capitalisation. I am the Company Secretary. The checklist should cover all three sections of the prescribed BRSR format: Section A (General Disclosures — company details, products, employees, CSR spends), Section B (Management and Process Disclosures — policies, governance structures, grievance mechanisms for each of the 9 NGRBC principles), and Section C (Principle-wise Performance Disclosures — Core and Comprehensive indicators). For each NGRBC Principle, list 3 to 5 essential disclosure items, the applicable BRSR section (Core or Comprehensive), the internal data source / verification method, and the team responsible for data collection. Format as a table: NGRBC Principle | Disclosure Item | Section (Core/Comprehensive) | SEBI Reference | Data Source / Verification | Responsible Owner. Cite SEBI Circular SEBI/HO/CFD/CMD-2/P/CIR/2021/562 where applicable."*

---

**Use Case: BRSR Core — Assurance Readiness Assessment**

> *"Assess the readiness of a listed company's BRSR disclosures for obtaining 'reasonable assurance' on BRSR Core indicators as mandated by SEBI for the top 1,000 listed entities from FY 2024-25. I am the Company Secretary coordinating with the Sustainability and Finance teams. The assessment should cover: (1) identification of all 9 BRSR Core Key Performance Indicators (KPIs) across environmental (GHG Scope 1 and Scope 2 emissions, energy intensity, water withdrawal, waste generated), social (LTIFR, employee well-being coverage, gender pay ratio), and governance (anti-corruption training, transparency of payments to government) dimensions; (2) data collection gaps and current internal control weaknesses; (3) recommended documentation standards for an independent assurance provider (CA / SEBI-registered ESG rating provider); and (4) timeline for completing the assurance process before Annual Report sign-off. Think step-by-step. Format as a gap assessment table: KPI | Current Data Availability | Gap Identified | Recommended Action | Assurance Standard (ISAE 3000 / AA1000AS). Cite the SEBI BRSR Core framework and SEBI circular of 2023 on assurance."*

---

**Use Case: ESG Policy Framework — Board Advisory Note**

> *"Draft a board advisory note recommending the adoption of a comprehensive ESG Policy for a listed public company. I am the Company Secretary advising the Board and ESG / Sustainability Committee. The note should cover: (1) business case for ESG — link to SEBI regulatory compliance, institutional investor expectations, and ESG rating agencies (MSCI, Sustainalytics, CRISIL ESG); (2) key pillars of the proposed ESG Policy — Environmental (energy transition, net-zero commitment timeline, water stewardship, waste management), Social (workforce diversity under POSH Act 2013, supply chain labour standards, community development aligned with Schedule VII CSR), and Governance (Board ESG oversight mechanism, anti-bribery and corruption policy under Prevention of Corruption Act 1988, whistleblower policy under Section 177(9) of the Companies Act 2013 and Regulation 22 of SEBI LODR); (3) integration with the existing CSR Policy under Section 135; (4) recommended governance structure — Board-level ESG Committee or delegation to Audit / CSR Committee; (5) annual BRSR reporting cycle and external assurance plan; and (6) an implementation roadmap with quarterly milestones. Think step-by-step. Use formal language suitable for board circulation."*

---

**Use Case: ESG Risk Assessment in M&A Due Diligence**

> *"Analyse ESG risks in a proposed merger or acquisition involving an Indian listed company under Sections 230–232 of the Companies Act 2013 and relevant SEBI regulations. I am the Company Secretary conducting pre-merger due diligence on behalf of the acquirer. Based on the attached due diligence materials [upload document], identify potential ESG red flags across three dimensions: (1) Environmental — regulatory violations under the Environment Protection Act 1986, Water (Prevention and Control of Pollution) Act 1974, Air Act 1981, pending environmental clearances (EIA Notification 2006), carbon-intensive assets or pending penalty notices from CPCB/SPCB; (2) Social — pending labour disputes under the Industrial Disputes Act 1947, POSH committee compliance (Sexual Harassment of Women at Workplace Act 2013), supply chain practices, community displacement issues; (3) Governance — anti-bribery compliance under Prevention of Corruption Act 1988, related party transaction irregularities under Section 188, pending SEBI enforcement actions, board independence deficits. Present findings in a table: ESG Dimension | Risk Description | Severity (High/Medium/Low) | Impact on Transaction Valuation or Regulatory Approvals | Mitigation Recommendation | Legal / Regulatory Reference. Restrict analysis strictly to the attached document. Do not introduce external assumptions."*

---

**Use Case: ESG Disclosure in Annual Report — Board Report Section**

> *"Draft the ESG-related disclosures for inclusion in the Board's Report of a listed public company for the financial year ended 31 March [YEAR], under Section 134(3)(o) (CSR), Section 134(3)(m) (energy conservation and technology absorption), and Regulation 34(2)(f) (BRSR) of SEBI LODR Regulations 2015. I am the Company Secretary. The disclosures should cover: (1) a brief narrative on the company's sustainability philosophy and ESG commitments, (2) summary of BRSR Core KPI performance for the year (GHG emissions, energy intensity, water consumption, LTIFR, gender diversity ratio, anti-corruption training coverage), (3) link to the full BRSR (as permitted under the MCA general circular allowing web-link references), (4) CSR spend summary and outcome measurement under the CSR Rules 2014 (as amended 2021), and (5) details of the ESG / Sustainability Committee or equivalent board oversight mechanism. Use formal Annual Report language. Indicate placeholders for actual data to be inserted. Do not fabricate figures."*

---

**Use Case: Responding to ESG Queries from Institutional Investors**

> *"Draft a formal response to ESG-related queries received from an institutional investor / foreign portfolio investor (FPI) ahead of the Annual General Meeting. I am the Company Secretary. The investor has raised the following specific concerns [paste investor queries]: board gender diversity, GHG emission reduction targets, supply chain labour practices, and executive remuneration linkage to ESG metrics. The response should: (1) address each query factually with reference to the company's BRSR / Annual Report disclosures, (2) cite the applicable regulatory framework (SEBI LODR, Companies Act 2013) and NGRBC principles where relevant, (3) describe any board-approved targets or timelines, and (4) invite the investor to the AGM to engage further with the management. Use formal, investor-relations-appropriate language. Do not include forward-looking statements without a suitable disclaimer."*

---

## 8. Extension to Other Jurisdictions

### 8.1 Singapore (ACRA / Companies Act Cap. 50)

**Key Regulatory Anchors:** Singapore Companies Act (Cap. 50), ACRA (Accounting and Corporate Regulatory Authority), SGX Listing Rules (for listed companies), SGX Mainboard / Catalist requirements, PDPA 2012, **SGX Sustainability Reporting requirements (SGX Listing Rules 711A/711B — mandatory for all listed issuers from FY 2022).**

**Adapting India Prompts for Singapore — Substitution Guide:**

| India Reference | Singapore Equivalent |
|---|---|
| Companies Act 2013 | Singapore Companies Act (Cap. 50) |
| MCA / ROC | ACRA / BizFile+ portal |
| SEBI LODR | SGX Listing Rules (Mainboard / Catalist) |
| Secretarial Standard SS-1/SS-2 | Companies Act Cap. 50 (Sections 173–184 for meetings) |
| ICSI / PCS | SAICSA (Singapore Association of the Institute of Chartered Secretaries) |
| MGT-7 (Annual Return) | ACRA Annual Return (BizFile+ e-filing) |
| DIR-12 | ACRA Form 45 (Consent to Act as Director) |
| MGT-14 | ACRA CORENET / BizFile+ |

**Sample Prompt — Singapore Annual Return:**

> *"Analyse the draft annual return for a Singapore private company limited by shares under Section 197 of the Singapore Companies Act (Cap. 50). I am the Company Secretary. Identify any gaps or missing disclosures. Present findings in a table: Item | ACRA Requirement | Description of Gap | Suggested Correction. Base the review on ACRA's BizFile+ annual return requirements and the Companies Act Cap. 50."*

---

**Sample Prompt — SGX Listing Compliance Calendar:**

> *"Generate a quarterly compliance calendar for a SGX Mainboard-listed company under the SGX Listing Rules. I am the Company Secretary. Cover: Rule 703 (immediate disclosure), Rule 704 (periodic disclosure), Rule 705 (quarterly/half-yearly/annual financial results), Rule 720 (directors' continuing obligations), and Rule 1207 (annual report disclosures). Format as a table: Month | Obligation | SGX Rule Number | Deadline | Filing Platform."*

---

**Sample Prompt — Singapore Sustainability Reporting (SGX Rules 711A/711B):**

> *"Generate a compliance checklist for preparing the Sustainability Report for a SGX Mainboard-listed company under SGX Listing Rules 711A and 711B. I am the Company Secretary. The report must follow TCFD-aligned disclosures (mandatory from FY 2023 for financials, energy, transport, and materials sectors; all issuers from FY 2025). The checklist should cover: (1) governance disclosures (board oversight of climate risks), (2) strategy disclosures (climate-related risks and opportunities, scenario analysis), (3) risk management (process for identifying and assessing climate risks), and (4) metrics and targets (Scope 1, Scope 2, Scope 3 GHG emissions where material, energy consumption). Format as a table: TCFD Pillar | Disclosure Requirement | SGX Rule Reference | Data Source | Status."*

---

### 8.2 United Kingdom (Companies House / Companies Act 2006)

**Key Regulatory Anchors:** UK Companies Act 2006, Companies House, FCA (for listed companies), UK Corporate Governance Code (FRC), Disclosure Guidance & Transparency Rules (DTR), Listing Rules (UKLR), **UK Streamlined Energy and Carbon Reporting (SECR) Regulations 2019 (mandatory for large companies), TCFD-aligned disclosures mandatory for UK premium-listed companies from FY 2021 (FCA PS21/23), UK Sustainability Disclosure Standards (UK SDS — ISSB-aligned, under adoption).**

| India Reference | UK Equivalent |
|---|---|
| Companies Act 2013 | Companies Act 2006 |
| RoC / MCA | Companies House |
| SEBI LODR | FCA Listing Rules / DTR |
| MGT-7 (Annual Return) | Confirmation Statement (CS01) |
| DIR-12 | Form AP01 (Director appointment) |
| Secretarial Audit | Company Secretarial Compliance Review |
| Section 135 CSR | Non-Financial Reporting (Sections 414C-414D CA 2006) |

**Sample Prompt — UK Confirmation Statement:**

> *"Generate a pre-filing compliance checklist for submitting the annual Confirmation Statement (Form CS01) to Companies House for a UK private limited company under Section 853A of the Companies Act 2006. I am the Company Secretary. Cover: (1) registered office address confirmation, (2) people with significant control (PSC) register verification under Part 21A, (3) SIC code confirmation, (4) shareholder list (if changed), (5) share capital statement, (6) filing deadline (within 14 days of the review period end date), and (7) filing fee. Include section references."*

---

**Sample Prompt — UK Board Minutes Compliance:**

> *"Draft board meeting minutes for a UK public limited company under the Companies Act 2006. I am the Company Secretary. The minutes should comply with Section 248 CA 2006 (which requires board minutes to be kept for 10 years) and the UK Corporate Governance Code 2018 (Principle E — formal and transparent board procedures). Include: chair's opening, attendance, quorum, approval of previous minutes, agenda items with outcomes, voting record, and director conflicts of interest under Section 177 CA 2006. Use formal, third-person language."*

---

**Sample Prompt — UK TCFD / SECR Compliance:**

> *"Summarise the mandatory climate-related disclosure requirements for a UK premium-listed company under: (1) FCA's TCFD-aligned Disclosure Rules (LR 9.8.6R and DTR 7.2.7AR), (2) the UK Streamlined Energy and Carbon Reporting (SECR) Regulations 2019 under Schedule 7 of the Companies Act 2006 (as amended), and (3) the UK Corporate Governance Code 2018 Principle A (long-term value and sustainability). I am the Company Secretary preparing the Annual Report. For each requirement, specify: what must be disclosed, where in the Annual Report it must appear, any numerical thresholds or materiality standards, and the consequences of non-disclosure. Present as a structured compliance table."*

---

### 8.3 United States (SEC / State Corporate Laws)

**Key Regulatory Anchors:** Delaware General Corporation Law (DGCL) or applicable state law, SEC Exchange Act (Sections 13 and 16 for reporting), SEC Regulation S-K (annual/periodic disclosures), NYSE/Nasdaq Listed Company Manuals, Dodd-Frank Act, SOX 2002.

| India Reference | US Equivalent |
|---|---|
| Companies Act 2013 | DGCL (Delaware) / Model Business Corporation Act (MBCA) |
| SEBI / Stock Exchange | SEC / NYSE / Nasdaq |
| SEBI LODR | SEC Exchange Act Reporting (10-K, 10-Q, 8-K) |
| MGT-7 Annual Return | Annual Proxy Statement (DEF 14A) + 10-K |
| Related Party Transactions | Item 404 Regulation S-K |
| Section 135 CSR | Non-binding ESG / proxy disclosures |

**Sample Prompt — SEC Section 16 Compliance:**

> *"Summarise the insider trading reporting obligations under Section 16 of the Securities Exchange Act of 1934 for directors and officers of an SEC-reporting company. I am the Corporate Secretary. Cover: (1) Form 3 (initial statement of beneficial ownership — due within 10 days of becoming an insider), (2) Form 4 (changes in ownership — due within 2 business days of transaction), (3) Form 5 (annual statement — due 45 days after fiscal year end for deferred transactions), (4) short-swing profit disgorgement under Section 16(b), and (5) company's obligation to post Section 16 filings on its website. Present as a compliance quick reference card."*

---

**Sample Prompt — Proxy Statement (DEF 14A) Outline:**

> *"Generate an outline for an Annual Meeting Proxy Statement (Form DEF 14A) for a Nasdaq-listed US company under SEC Regulation 14A. I am the Corporate Secretary. The proxy proposals are: (1) election of directors (majority voting standard), (2) ratification of independent auditor, (3) say-on-pay advisory vote under Dodd-Frank Section 951, and (4) shareholder proposal on proxy access. The outline should list each required disclosure item under Schedule 14A / Regulation S-K, including: Director biographies and independence, executive compensation tables (Summary Compensation Table, Grants of Plan-Based Awards, Outstanding Equity Awards), pay ratio disclosure (Item 402(u)), and audit committee report. Indicate which sections require EDGAR filing in XBRL format."*

---

### 8.4 UAE (DIFC / ADGM)

**Key Regulatory Anchors:** UAE Companies Law (Federal Law No. 32 of 2021), DIFC Companies Law (DIFC Law No. 5 of 2018), ADGM Companies Regulations 2020, UAE Securities and Commodities Authority (SCA) for listed entities, ADX/DFM Listing Rules.

**Sample Prompt — UAE Federal Company Compliance:**

> *"Summarise the obligations of a Limited Liability Company (LLC) under UAE Federal Law No. 32 of 2021 (Companies Law) for holding annual general meetings. I am advising the corporate secretary of a UAE mainland LLC. Cover: (1) requirement to hold AGM within 4 months of financial year end (Article 132), (2) notice period to partners (21 days), (3) quorum requirements, (4) matters requiring unanimous or supermajority approval, and (5) filing of resolutions with the relevant licensing authority (DED). Note any differences under DIFC or ADGM frameworks where applicable."*

---

## 9. Copilot Prompt Examples (Microsoft 365)

The following sample prompts are designed for Microsoft 365 Copilot in applications commonly used by Company Secretaries.

### Microsoft Word

- "Analyse the attached board minutes [reference file in OneDrive] and extract all compliance action items into a table with columns: Action Item | Applicable Law/SS | Deadline | Responsible Officer | Status. Comment on whether the minutes comply with Secretarial Standard SS-1 issued by ICSI."

- "Redraft the Directors' Responsibility Statement in this Annual Report [reference file] in formal legal language under Section 134(5) of the Companies Act 2013. Ensure all five sub-clauses are addressed."

### Microsoft Teams

- "Please recap this board meeting and create a table of resolutions passed, with columns: Resolution Number | Subject | Type (Ordinary/Special) | Voting Outcome | Follow-Up Action Required."

- "Convert the transcript of today's Audit Committee meeting into structured minutes. Identify all audit observations discussed, management responses, and committee recommendations with responsible persons and timelines."

### Microsoft PowerPoint

- "Create a board presentation on SEBI LODR compliance status for a listed company. Include slides for: (1) Executive Summary of pending compliance items, (2) Board Composition adequacy under Regulation 17, (3) Q3 financial results timeline under Regulation 33, (4) Insider Trading policy updates, and (5) upcoming AGM action plan. Keep language formal and concise."

- "Generate a training presentation for newly appointed Independent Directors on their fiduciary duties under Section 149 and Schedule IV (Code for Independent Directors) of the Companies Act 2013. Include separate slides for each key obligation and a Q&A checklist slide."

### Microsoft Outlook

- "Summarise all emails in this thread regarding the FEMA FC-GPR filing and identify any outstanding items, documents yet to be received, and approaching deadlines. Present as a brief action summary."

- "I have been travelling for a week. Summarise all compliance-related emails I have received, prioritising those relating to SEBI disclosures, MCA filings, and board/shareholder meeting deadlines."

### Microsoft Edge

- "Summarise this SEBI circular [URL] for a compliance update to be presented to the Audit Committee. Focus on: applicability, effective date, compliance obligations, and implications for the company's existing policies."

- "Compare the corporate governance requirements on board independence under [Regulation 17 SEBI LODR URL] and [UK Corporate Governance Code URL]. Highlight key differences in thresholds, cooling-off periods, and performance evaluation requirements."

---

## 10. Chaining Prompts — Workflow Sequences

Complex CS tasks benefit from chaining multiple prompts in sequence within the same conversation, each building on the previous output. Here are two end-to-end sequences:

### Sequence A: Board Meeting End-to-End

```
PROMPT 1 (Plan):
"List all agenda items and mandatory SS-1 compliance steps for a board meeting 
of a listed company approving quarterly results under Reg. 33 SEBI LODR. 
Output as a numbered checklist with section references."

PROMPT 2 (Notice):
"Using the checklist above, draft the formal Notice convening this board meeting 
under Section 173(3) of the Companies Act 2013 and Clause 1.3 of SS-1. 
The meeting is via VC. 7 days advance notice."

PROMPT 3 (Agenda):
"Now draft the detailed Board Agenda for this meeting. 
Include all regulatory disclosures required to be tabled."

PROMPT 4 (Resolution):
"Draft the board resolution for approval and adoption of the unaudited 
quarterly financial results under Regulation 33 of SEBI LODR, 
to be published in a newspaper and submitted to BSE/NSE within 45 minutes 
of conclusion of the board meeting."

PROMPT 5 (Post-meeting):
"Generate the post-meeting compliance action checklist: 
what must be filed with MCA, SEBI, stock exchanges, 
and what updates must be made to statutory registers within what deadlines."
```

---

### Sequence B: Annual Return Filing End-to-End

```
PROMPT 1 (Gap analysis):
"Analyse this draft MGT-7 form [paste content]. Identify all gaps 
under Section 92 and Companies (Management and Administration) Rules 2014."

PROMPT 2 (Correction table):
"For each gap identified, generate a correction table: 
Field | Required Content | Current Content | Suggested Correction | Source."

PROMPT 3 (Declarations):
"Generate the list of all declarations / certifications required 
from directors and KMPs before the MGT-7 can be certified by a PCS."

PROMPT 4 (Covering letter):
"Draft a professional covering note from the CS to the MD 
summarising the corrections required and requesting sign-off 
before the annual return is filed."

PROMPT 5 (Filing checklist):
"Generate the final pre-filing checklist for MCA21 portal submission 
of MGT-7, including digital signature requirements (DSC Class 3), 
attachments, and SRN tracking."
```

---

### Sequence C: BRSR / ESG Annual Reporting End-to-End

```
PROMPT 1 (Gap Assessment):
"Review the attached last year's BRSR [upload document]. Identify 
all Core KPIs where data was not reported or marked N/A. 
Format as a gap table: KPI | NGRBC Principle | Gap | Root Cause."

PROMPT 2 (Data Collection Plan):
"Using the gap table above, generate an internal data collection 
plan. For each KPI gap, assign: Data Owner (Finance/HR/Operations/EHS), 
Data Source, Collection Method, and Deadline. 
Format as a project tracker table."

PROMPT 3 (BRSR Narrative Draft):
"Draft the Management and Process Disclosures (Section B of BRSR) 
for NGRBC Principles 1, 6, and 8 for a listed manufacturing company. 
Base on the following policy documents [paste summaries]. 
Use formal language consistent with an Annual Report. 
Indicate placeholders for actual metrics."

PROMPT 4 (Board Note):
"Summarise the key ESG performance highlights and regulatory 
compliance status (BRSR Core assurance readiness) in a 
Board Advisory Note format. Include 3 recommendations 
for the next financial year. Formal language, 1 page."

PROMPT 5 (Investor Communication):
"Draft a brief ESG performance summary (250 words) suitable 
for investor relations use — highlighting BRSR Core KPI outcomes, 
initiatives under Schedule VII CSR, and TCFD-aligned 
climate disclosures. Use plain, factual language."
```

---

## 11. Glossary of Key Terms

**BRSR.** Business Responsibility and Sustainability Report — a mandatory sustainability disclosure document required under Regulation 34(2)(f) of SEBI LODR Regulations 2015 for the top 1,000 listed entities by market capitalisation in India. Structured around the 9 NGRBC Principles and divided into Core (subject to assurance) and Comprehensive indicators.

**ESG.** Environmental, Social, and Governance — the three pillars used to assess the sustainability and ethical impact of a company. For Indian listed companies, ESG is operationalised primarily through BRSR reporting, CSR obligations, and board governance requirements under SEBI LODR and the Companies Act 2013.

**Chain-of-Thought Prompting.** A prompting technique where the user instructs the AI to "think step-by-step" through a problem, producing higher quality reasoning for complex compliance or legal analysis tasks.

**Context.** The surrounding information in a prompt that helps the AI understand the background, jurisdiction, applicable law, and parties involved.

**CIN.** Corporate Identity Number — the unique identifier assigned to a company by the Registrar of Companies under the Companies Act 2013. Always anonymise before using in non-enterprise AI tools.

**Few-Shot Learning.** A prompting approach where the user provides one or more examples of the desired output style within the prompt, enabling the AI to emulate that format.

**Generative AI.** A type of AI that can generate novel content — text, tables, summaries, draft documents, code — based on training data and prompts.

**ICSI.** The Institute of Company Secretaries of India — the statutory professional body that issues Secretarial Standards and regulates CS professionals in India.

**MCA21.** The Ministry of Corporate Affairs' digital e-filing platform for Indian company law compliance.

**Model.** The trained AI program that understands and generates text — the "brain" of the generative AI system.

**Output.** The AI system's response to a prompt.

**Prompt.** The text input provided to an AI system to direct its output. Well-structured prompts follow the Goal → Context → Expectations → Source framework.

**Secretarial Standard.** Mandatory standards issued by ICSI (SS-1 for Board Meetings, SS-2 for General Meetings) that govern how meetings of companies should be conducted and documented.

**Token.** The unit by which AI models process text — roughly equivalent to a word fragment. AI models have context window limits measured in tokens.

**NGRBC.** National Guidelines on Responsible Business Conduct — 9 principles issued by the Ministry of Corporate Affairs covering ethics, environment, human rights, governance, and stakeholder engagement. BRSR disclosures are structured principle-by-principle against the NGRBC.

**TCFD.** Task Force on Climate-related Financial Disclosures — an internationally recognised framework for voluntary (and, for some jurisdictions, mandatory) climate-related disclosures structured around four pillars: Governance, Strategy, Risk Management, and Metrics & Targets. Required for UK premium-listed companies and Singapore-listed issuers; referenced in India's BRSR Core framework. — information relating to a listed company that, if published, would materially affect the price of its securities. Trading on UPSI is prohibited under SEBI (PIT) Regulations 2015.

---

## 12. Quick Reference Card

### The CS Prompt Formula

> **[ACTION VERB] + [DOCUMENT/TASK] + [COMPANY TYPE] + [APPLICABLE LAW/SS] + [FORMAT REQUIRED] + [CITATIONS REQUIRED]**

| Element | Good Examples | Weak Examples |
|---|---|---|
| Action Verb | Draft, Analyse, Generate, Review, Identify, Summarise, Extract | "Help me with", "Tell me about" |
| Specificity | "Form MGT-7 for a listed public company" | "Annual return form" |
| Law Reference | "Section 177 Companies Act 2013 + Reg. 18 SEBI LODR" | "SEBI rules" |
| Format | "Table with 5 columns: Item, Section, Gap, Correction, Priority" | "Give me a list" |
| Citation Request | "Cite specific section and regulation numbers throughout" | (Omitting this) |
| Chain-of-Thought | "Think step-by-step. First identify, then analyse, then recommend." | Single vague request |
| ESG-specific | "Based on NGRBC Principle 6, BRSR Core, SEBI Circular 2021/562" | "ESG stuff for the annual report" |

### India CS Compliance — Key Deadlines Reference

| Filing / Obligation | Form | Deadline | Law Reference |
|---|---|---|---|
| Annual Return (Listed Co.) | MGT-7 | Within 60 days of AGM | Section 92(4) |
| Financial Statements | AOC-4 | Within 30 days of AGM | Section 137(1) |
| Director Change | DIR-12 | Within 30 days of change | Rule 15 |
| Charge Creation | CHG-1 | Within 30 days (extendable to 60) | Section 77(1) |
| Board Resolution (certain) | MGT-14 | Within 30 days of resolution | Section 117(1) |
| FDI Reporting | FC-GPR (FIRMS) | Within 30 days of allotment | FEMA NDI Rules |
| Secretarial Audit Report | MR-3 (annexed to Board Report) | With Annual Report | Section 204 |
| CSR Report | Board Report Annexure + CSR-2 | With Annual Report | Section 135 + Rule 12(2) |
| BRSR Filing | Annexed to Annual Report | With Annual Report (top 1,000 listed cos.) | SEBI LODR Reg. 34(2)(f) |
| BRSR Core Assurance | Obtained before Annual Report sign-off | FY 2024-25 onwards (top 1,000) | SEBI Circular 2023 |
| MSME Half-Yearly Return | MSME-1 | 31 Oct / 30 Apr | MSME Order 2019 |
| DPT-3 Return of Deposits | DPT-3 | On or before 30 June | Rule 16 |
| SBO Filing | BEN-2 | Within 30 days of receipt of BEN-1 | Rule 4(3) |
| Insider Trading Initial Disclosure | Form B (PIT) | Within 7 trading days of becoming insider | Regulation 7(2)(a) |
| Quarterly Compliance Report (Listed) | Annex to BSE/NSE | Within 21 days of quarter end | Regulation 27(2) LODR |
| Material Event Disclosure (Listed) | BSE/NSE filing | Within 24 hours (30 min for board outcomes) | Regulation 30 LODR |
| RPT Prior Approval (Listed) | Audit Committee + Board | Before transaction | Regulation 23 LODR |

---

## Acknowledgements

This guide draws on the regulatory frameworks of the Ministry of Corporate Affairs (MCA), the Securities and Exchange Board of India (SEBI), the Institute of Company Secretaries of India (ICSI), the Reserve Bank of India (RBI), and equivalent bodies in Singapore (ACRA), the United Kingdom (Companies House / FCA), and the United States (SEC / NYSE / Nasdaq). The prompt engineering framework is inspired by best practices established in professional services AI adoption, including the *Prompt Engineering for Lawyers* guide by Microsoft and the Singapore Academy of Law (2024), adapted and extended for corporate secretarial practice.

Company Secretaries using this guide are reminded that all AI-generated output must be independently verified against primary legal sources before use in filings, disclosures, board communications, or client advice. The authors make no warranties as to the legal accuracy of AI-generated outputs.

---

*This guide is intended for educational and professional development purposes. Always refer to the latest amendments and circulars from MCA, SEBI, ICSI, and RBI before acting on any compliance matter.*