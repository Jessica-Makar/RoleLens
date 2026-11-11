# RoleLens – AI-Powered Resume Analyzer

**See your potential. Find your next opportunity.**

RoleLens is an AI-powered resume analysis application that evaluates how well a candidate's resume aligns with a job description. Using Claude AI, Python, and Streamlit, the application identifies relevant skills, verifies qualifications through resume evidence, highlights missing requirements, and generates actionable recommendations to help candidates better understand their job fit.


## Application Screenshots

### Home Screen
![RoleLens Home Screen](screenshots/home1.png)
![RoleLens Home Screen](screenshots/home2.png)

### Resume Analysis Dashboard
![RoleLens Analysis Dashboard](screenshots/dashboard.png)

### Generated PDF Report
![RoleLens PDF Report](screenshots/report.png)

## Features

- **Resume Parsing:** Upload PDF and DOCX resumes for automatic text extraction.
- **AI-Powered Analysis:** Analyze resumes against job descriptions using Anthropic's Claude API.
- **Resume Match Scoring:** Generate an overall match score based on four evaluation categories:
  - Technical Skills (40%)
  - Relevant Experience (30%)
  - Education (15%)
  - Other Requirements (15%)
- **Skill Verification:** Classify skills as verified, unverified, matching, or missing based on resume content and supporting evidence.
- **Experience Analysis:** Identify relevant experience, strengths, and areas for improvement.
- **Actionable Recommendations:** Generate suggestions to improve resume alignment with job requirements.
- **Interactive Dashboard:** View match scores, score breakdowns, and detailed analysis in an organized interface.
- **Report Generation:** Download analysis results as PDF and JSON files.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Streamlit | Interactive web interface |
| Anthropic Claude API | AI-powered resume analysis |
| pypdf | PDF text extraction |
| python-docx | DOCX text extraction |
| ReportLab | PDF report generation |
| python-dotenv | Environment variable management |
| pytest | Automated testing |

## Project Structure

```text
RoleLens/
├── .streamlit/
│   └── config.toml
├── data/
│   └── sample_resumes/
├── prompts/
│   └── resume_analysis.txt
├── src/
│   ├── branding.py
│   ├── claude_analyzer.py
│   ├── report_generator.py
│   └── resume_parser.py
├── tests/
│   ├── test_analyzer.py
│   ├── test_resume_parser.py
│   └── test_skill_validation.py
├── .env.example
├── .gitignore
├── app.py
├── create_sample.py
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- An Anthropic API key

### 1. Clone the Repository

```bash
git clone https://github.com/Jessica-Makar/RoleLens.git
cd RoleLens
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory using `.env.example` as a reference.

Add your Anthropic API key:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## Running Tests

Run the automated test suite from the project root:

```bash
pytest -v
```

## How It Works

1. The user uploads a resume in PDF or DOCX format.
2. RoleLens extracts and cleans the resume text.
3. The user provides a job description.
4. The application sends the resume content and job description to Claude for structured analysis.
5. The analysis is validated and used to calculate the overall match score.
6. Results are displayed in an interactive dashboard.
7. The user can download the analysis as a PDF or JSON report.

## Privacy and Security

- API credentials are stored in environment variables and should never be committed to the repository.
- Resume content is processed through the Anthropic API for analysis.
- Users should avoid uploading sensitive personal information unless they understand and accept the applicable data-handling practices.

## Future Improvements

Potential enhancements include:
- Resume improvement and rewriting assistance.
- Comparison of multiple resumes against one job description.
- More detailed job-specific skill recommendations.
- Additional analysis and reporting options.

## Disclaimer

RoleLens provides AI-generated resume feedback for informational purposes. Match scores and recommendations are estimates and should not be treated as guarantees of employment or hiring decisions.

## Author

**Jessica Makar**

Computer Science & Data Science Graduate | Rutgers University

[GitHub](https://github.com/Jessica-Makar)