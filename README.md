# RoleLens – AI-Powered Resume Analyzer

**See your potential. Find your next opportunity.**

[![Live Application](https://img.shields.io/badge/Live%20App-RoleLens-blue?style=for-the-badge)](https://rolelens-ai.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/Jessica-Makar/RoleLens)

RoleLens is an AI-powered resume analysis application that evaluates how well a candidate's resume aligns with a job description. Using Python, Streamlit, Anthropic's Claude API, and Supabase, the application identifies relevant skills, verifies qualifications through resume evidence, highlights missing requirements, and generates actionable recommendations.

## Live Demo

**[Launch RoleLens](https://rolelens-ai.streamlit.app/)**

Upload a PDF or DOCX resume, paste a job description, and receive an AI-generated analysis of your qualifications and job alignment.

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
- **Interactive Dashboard:** View match scores, score breakdowns, skill classifications, and detailed analysis.
- **Report Generation:** Download analysis results as PDF and JSON files.
- **Usage Tracking:** Track daily analysis usage through Supabase.
- **Usage Limits:** Enforce a limit of 2 analysis reservations per visitor per day and 10 across all visitors per UTC day.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Streamlit | Interactive web interface |
| Anthropic Claude API | AI-powered resume analysis |
| Supabase | Database and usage tracking |
| PostgreSQL | Usage tracking database |
| pandas | Data processing |
| pypdf | PDF text extraction |
| python-docx | DOCX text extraction |
| ReportLab | PDF report generation |
| python-dotenv | Environment variable management |
| pytest | Automated testing |
| Git & GitHub | Version control and project hosting |

## Project Structure

```text
RoleLens/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml          # Local only; not committed
├── data/
│   └── sample_resumes/
├── prompts/
│   └── resume_analysis.txt
├── screenshots/
│   ├── home1.png
│   ├── home2.png
│   ├── dashboard.png
│   └── report.png
├── src/
│   ├── __init__.py
│   ├── branding.py
│   ├── claude_analyzer.py
│   ├── report_generator.py
│   ├── resume_parser.py
│   └── usage_limiter.py
├── supabase/
│   └── setup.sql
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

- Python 3.14
- Git
- An Anthropic API key
- A Supabase project

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

### 5. Configure Supabase

1. Create a Supabase project.
2. Open the SQL Editor in your Supabase dashboard.
3. Open `supabase/setup.sql` from this repository.
4. Copy its contents into the Supabase SQL Editor and execute the script.
5. Create `.streamlit/secrets.toml` locally and add your Supabase credentials:

```toml
[supabase]
url = "YOUR_SUPABASE_PROJECT_URL"
service_role_key = "YOUR_SUPABASE_SERVICE_ROLE_KEY"
```

The Supabase service role key must remain private and should never be committed to GitHub.

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## Deployment

RoleLens is deployed using Streamlit Community Cloud.

**Live Application:** https://rolelens-ai.streamlit.app/

To deploy your own instance:

1. Push the project to a GitHub repository.
2. Connect the repository to Streamlit Community Cloud.
3. Set the main file path to `app.py`.
4. Configure the following secrets in the app's Advanced Settings:

```toml
ANTHROPIC_API_KEY = "YOUR_ANTHROPIC_API_KEY"

[supabase]
url = "YOUR_SUPABASE_PROJECT_URL"
service_role_key = "YOUR_SUPABASE_SERVICE_ROLE_KEY"
```

5. Deploy the application.

## Running Tests

Run the automated test suite from the project root:

```bash
pytest -v
```

The project includes 14 automated tests covering analysis validation, resume parsing, and skill classification consistency.

## How It Works

1. The user uploads a resume in PDF or DOCX format.
2. RoleLens extracts and cleans the resume text.
3. The user provides a job description.
4. The application retrieves the visitor's usage allowance through Supabase.
5. If the visitor is within the usage limits, the resume and job description are sent to Claude for structured analysis.
6. The analysis is validated and used to calculate the overall match score.
7. Results are displayed in an interactive dashboard.
8. The user can download the analysis as a PDF or JSON report.

## Usage Limits

RoleLens uses Supabase to enforce daily usage limits:

- **Visitor limit:** 2 analysis reservations per visitor per day.
- **Global limit:** 10 analysis reservations across all visitors per day.
- **Reset schedule:** Limits reset at midnight UTC.
- **Visitor identification:** An anonymous UUID is stored in the URL query parameter.

The visitor UUID is not a verified identity and can be changed or bypassed. The global limit provides an additional layer of usage protection.

## Privacy and Security

- API credentials are stored in environment variables or Streamlit Secrets and should never be committed to the repository.
- The Supabase service role key is used server-side only.
- Row Level Security (RLS) is enabled on the usage tracking table.
- Resume content is processed through the Anthropic API for analysis.
- Uploaded resume information should be treated as sensitive personal data. Users should avoid uploading information they do not wish to submit for AI processing.

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

[GitHub](https://github.com/Jessica-Makar) | [LinkedIn](https://www.linkedin.com/in/jessicamakar)