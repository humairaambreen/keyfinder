# Key Finder

A web-based tool for analyzing LinkedIn job postings to identify trending keywords, skills, and qualifications. Key Finder helps job seekers and recruiters understand what the market is looking for by extracting and ranking keywords from real job descriptions.

**Repository**: [github.com/humairaambreen/keyfinder](https://github.com/humairaambreen/keyfinder)
**Live URL**: [keyfinder-msnk.onrender.com](https://keyfinder-msnk.onrender.com)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [How It Works](#how-it-works)
- [Noise Word Filtering](#noise-word-filtering)
- [API Endpoints](#api-endpoints)
- [Export Functionality](#export-functionality)
- [Technical Stack](#technical-stack)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Key Finder is a Python-based web application that scrapes LinkedIn job postings, extracts keywords from job descriptions, and presents frequency analysis in an intuitive web interface. The tool is designed to help users identify the most in-demand skills and qualifications for specific job roles or industries.

### Key Capabilities

- Scrapes multiple pages of LinkedIn job search results
- Extracts and analyzes full job descriptions
- Filters out common noise words to focus on meaningful keywords
- Identifies single words, two-word phrases, and three-word phrases
- Provides real-time progress tracking during analysis
- Exports results to CSV format for further analysis
- Features a minimalist black-themed web interface

---

## Features

### Web Interface
- Clean, minimalist black-themed UI built with pure HTML/CSS/JavaScript
- No external CSS frameworks or dependencies
- Fully responsive design for desktop, tablet, and mobile devices
- Monospace typography for a technical aesthetic

### Real-time Progress Tracking
- Live progress bar showing analysis completion percentage
- Current page being analyzed and total pages
- Count of jobs found so far
- Display of the most recently discovered job title
- Status updates at each stage of the analysis

### Visual Results
- Keyword frequency displayed as counts and percentages
- Visual frequency bars for easy comparison
- Sortable table showing top keywords
- Summary statistics including total jobs analyzed and unique keywords found
- Top keyword frequency percentage highlighted

### Data Export
- Export keywords with frequency data to CSV
- Export complete job listings with titles, URLs, and descriptions to CSV
- Timestamped filenames for easy organization
- Ready for import into Excel, Google Sheets, or data analysis tools

### Customizable Noise Filtering
- External `noise.txt` file for easy customization
- Support for single words and multi-word phrases
- Comma-separated values on a single line
- No comment system for maximum simplicity

---

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Internet connection for scraping LinkedIn

### Step 1: Clone the Repository

```bash
git clone https://github.com/humairaambreen/keyfinder.git
cd keyfinder
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies

Option A - Recommended: Use the pinned `requirements.txt` file

```bash
pip install -r requirements.txt
```

Option B - Install packages manually (if you prefer)

```bash
pip install flask flask-cors requests beautifulsoup4 pandas
```

If you update or add dependencies while developing, regenerate `requirements.txt`:

```bash
pip freeze > requirements.txt
```

### Required Packages

The exact versions used by this project are pinned in `requirements.txt`. Installing from that file is recommended to ensure compatibility.

- **Flask** (2.0+): Web framework for the backend server
- **Flask-CORS**: Enables Cross-Origin Resource Sharing
- **Requests**: HTTP library for scraping web pages
- **BeautifulSoup4**: HTML parsing and web scraping
- **Pandas**: Data manipulation and CSV export

---

## Usage

### Starting the Application

1. Navigate to the project directory
2. Activate your virtual environment (if using one)
3. Run the main script:

```bash
python3 main.py
```

4. Open your web browser and navigate to:
```
http://localhost:5001
```

### Running an Analysis

1. **Enter Job Title or Keywords**
   - Type the job role you want to analyze (e.g., "Software Engineer", "Data Scientist", "Product Manager")
   - Be specific for more targeted results
   - Use quotes for exact phrases if needed

2. **Select Number of Pages**
   - Choose between 1-10 pages to analyze
   - Each page contains approximately 25 job postings
   - More pages = more comprehensive data but longer analysis time
   - Recommended: Start with 3-5 pages for quick insights

3. **Click "Start Analysis"**
   - The application will begin scraping LinkedIn
   - Progress will be displayed in real-time
   - Analysis typically takes 2-3 minutes per page

4. **Review Results**
   - Keywords are ranked by frequency
   - View percentage of jobs containing each keyword
   - Examine visual frequency indicators
   - Check summary statistics at the top

5. **Export Data**
   - Click "Export Keywords CSV" to download keyword frequency data
   - Click "Export Jobs CSV" to download complete job listings
   - Files are saved with timestamps for easy organization

6. **Run New Analysis**
   - Click "New Analysis" to start over with different parameters

---

## Configuration

### Port Configuration

The application runs on port 5001 by default. To change the port:

1. Open `main.py`
2. Find the last line: `app.run(debug=True, host='0.0.0.0', port=5001)`
3. Change `port=5001` to your desired port number

### Debug Mode

Debug mode is enabled by default for development. To disable for production:

Change `debug=True` to `debug=False` in the `app.run()` call.

### Host Configuration

The application binds to `0.0.0.0` by default, making it accessible from other devices on your network. To restrict to localhost only:

Change `host='0.0.0.0'` to `host='127.0.0.1'`

---

## Architecture

### Project Structure

```
keyfinder/
├── main.py                 # Flask application and core logic
├── noise.txt               # Noise words configuration file
├── templates/
│   └── index.html          # Web interface
├── requirements.txt        # Pinned Python dependencies
├── README.md               # This documentation
```

### Application Components

#### Backend (main.py)

1. **KeyFinder Class**
   - Manages keyword extraction and job analysis
   - Loads noise words from external file
   - Handles web scraping and data processing
   - Generates analysis results

2. **Background Processing**
   - Analysis runs in a separate thread
   - Non-blocking progress updates
   - Global state management for progress tracking

#### Frontend (index.html)

1. **HTML Structure**
   - Semantic markup for accessibility
   - Form for user input
   - Progress tracking section
   - Results display with table
   - Error and success messaging

2. **CSS Styling**
   - Pure black (#000000) background
   - White text with grayscale accents
   - Monospace typography (Courier New)
   - Minimalist borders and spacing
   - Responsive grid layout

3. **JavaScript Logic**
   - Form submission handling
   - AJAX requests for analysis and progress
   - Real-time UI updates via polling
   - CSV export functionality
   - Error handling and user feedback

---

## How It Works

### Analysis Pipeline

#### 1. Job Discovery
- Constructs LinkedIn search URL with user-specified keywords
- Iterates through the requested number of pages
- Extracts job card elements from search results
- Retrieves job URLs and titles

#### 2. Content Extraction
- Fetches full job description for each posting
- Parses HTML using BeautifulSoup
- Extracts text content from description sections
- Handles multiple HTML structure variations

#### 3. Keyword Extraction
- Converts text to lowercase for consistency
- Uses regex to clean text: `re.sub(r'[^\w\s\+\#\.]', ' ', text)`
- Preserves special characters: `+`, `#`, `.`
- Splits into individual words

#### 4. Single Word Processing
- Filters words by length (2-50 characters)
- Removes pure numeric values
- Excludes noise words from `noise.txt`
- Adds valid words to keyword set

#### 5. Phrase Detection
- **Two-word phrases**: Combines adjacent non-noise words
- **Three-word phrases**: Combines three consecutive non-noise words
- Checks complete phrases against noise word list
- Respects 50-character maximum length

#### 6. Frequency Calculation
- Counts job postings containing each keyword
- Calculates percentage across total jobs analyzed
- Filters keywords appearing in at least 2 jobs
- Sorts by frequency (descending)

#### 7. Result Presentation
- Returns structured data with keyword statistics
- Displays in web interface with visual indicators
- Provides export functionality

### Rate Limiting and Politeness

- 1-second delay between job description fetches
- 2-second delay between search result pages
- 10-second timeout for HTTP requests
- User-Agent header to identify requests

---

## Noise Word Filtering

### Purpose

Noise words are common terms that appear frequently in job postings but don't provide meaningful insights into specific requirements. Filtering these words allows Key Finder to focus on technical skills, tools, and qualifications.

### Configuration File: noise.txt

The `noise.txt` file contains words and phrases to exclude from analysis. It supports:

- **Single words**: One per line
- **Multi-word phrases**: Space-separated terms on one line
- **Comma-separated lists**: Multiple entries on a single line
- **Special characters**: `#`, `.`, `+`, numbers, etc.

### File Format

```
the
and
for
software engineer
100 000, 000 professionals, 3+, 40+
#coder
. previous
```

### Categories of Noise Words

1. **Basic English words**: the, and, for, with, are, this, that, etc.
2. **Job-related generic terms**: job, role, position, candidate, remote, etc.
3. **Benefits/compensation**: salary, benefits, medical, dental, 401k, etc.
4. **Legal/compliance**: equal employment, disability, veteran status, etc.
5. **Generic action words**: make, take, give, drive, grow, etc.
6. **Quality descriptors**: best, great, unique, innovative, etc.
7. **Tech/business generic**: technical, product, system, process, etc.
8. **Location terms**: located, office, workplace, site, etc.

### Customization

To customize noise word filtering:

1. Open `noise.txt` in a text editor
2. Add or remove words/phrases (one per line or comma-separated)
3. Save the file
4. Restart the Key Finder application
5. New analyses will use the updated noise word list

### How Filtering Works

The application checks:
1. Individual words against the noise list
2. Two-word phrases against the noise list
3. Three-word phrases against the noise list

A keyword is excluded if it matches any entry in `noise.txt`.

---

## API Endpoints

### GET /

**Description**: Serves the main web interface

**Response**: HTML page

---

### POST /analyze

**Description**: Initiates a new keyword analysis job

**Request Body**:
```json
{
  "keyword": "Software Engineer",
  "pages": 5
}
```

**Parameters**:
- `keyword` (string, required): Job title or search term
- `pages` (integer, required): Number of pages to analyze (1-10)

**Response**:
```json
{
  "status": "started"
}
```

**Status Codes**:
- 200: Analysis started successfully
- 400: Invalid request (missing keyword)

---

### GET /progress

**Description**: Retrieves real-time progress of the current analysis

**Response**:
```json
{
  "status": "running",
  "current_page": 3,
  "total_pages": 5,
  "jobs_found": 65,
  "current_job": "Senior Software Engineer",
  "results": null,
  "error": null
}
```

**Status Values**:
- `idle`: No analysis running
- `starting`: Analysis initialization
- `running`: Analysis in progress
- `completed`: Analysis finished successfully
- `error`: Analysis failed

**Response Fields**:
- `status`: Current status of the analysis
- `current_page`: Page currently being processed
- `total_pages`: Total pages to analyze
- `jobs_found`: Number of jobs discovered so far
- `current_job`: Title of the most recent job found
- `results`: Analysis results (only when status is "completed")
- `error`: Error message (only when status is "error")

---

### GET /export/keywords

**Description**: Exports keyword frequency data to CSV

**Response**: CSV file download

**Filename Format**: `keywords_<search_term>_<timestamp>.csv`

**CSV Columns**:
- Rank
- Keyword
- Jobs (count)
- Percentage

---

### GET /export/jobs

**Description**: Exports complete job listings to CSV

**Response**: CSV file download

**Filename Format**: `jobs_<search_term>_<timestamp>.csv`

**CSV Columns**:
- Title
- URL
- Description (truncated to 500 characters)

---

## Export Functionality

### Keywords CSV

Contains keyword frequency analysis:

```csv
Rank,Keyword,Jobs,Percentage
1,python,45,90.0%
2,machine learning,38,76.0%
3,aws,35,70.0%
```

Use cases:
- Identify most in-demand skills
- Compare keyword trends over time
- Create skill requirement charts
- Prioritize learning objectives

### Jobs CSV

Contains complete job listing data:

```csv
Title,URL,Description
Software Engineer,https://linkedin.com/jobs/view/123456,We are seeking a talented...
Senior Developer,https://linkedin.com/jobs/view/789012,Our team is looking for...
```

Use cases:
- Build a job application tracker
- Analyze job description patterns
- Create a database of relevant positions
- Reference specific requirements

---

## Technical Stack

### Backend Technologies

- **Python 3.7+**: Core programming language
- **Flask 2.0+**: Lightweight web framework
- **Flask-CORS**: Cross-origin resource sharing support
- **Requests**: HTTP library for web scraping
- **BeautifulSoup4**: HTML parsing and content extraction
- **Pandas**: Data manipulation and CSV export

### Frontend Technologies

- **HTML5**: Semantic markup
- **CSS3**: Styling with modern features (Grid, Flexbox)
- **JavaScript (ES6+)**: Client-side logic and interactivity
- **Fetch API**: AJAX requests for real-time updates

### Development Tools

- **Virtual Environment**: Isolated Python dependencies
- **Git**: Version control

---

## Troubleshooting

### Application Won't Start

**Error**: `Address already in use`

**Solution**: 
- Another process is using port 5001
- Kill the process: `kill -9 $(lsof -ti:5001)`
- Or change the port in `main.py`

---

### No Results Returned

**Possible Causes**:
- Too few pages selected
- Very specific/rare job title
- LinkedIn blocking requests
- Network connectivity issues

**Solutions**:
- Increase number of pages (try 5-10)
- Use broader search terms
- Check internet connection
- Wait a few minutes and try again

---

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Or manually: `pip install flask flask-cors requests beautifulsoup4 pandas`

---

### Slow Performance

**Causes**:
- LinkedIn rate limiting (intentional delays)
- Large number of pages
- Slow internet connection

**Expected Performance**:
- ~2-3 minutes per page
- ~10-15 minutes for 5 pages

**Note**: This is normal and intentional to respect LinkedIn's servers

---

### Noise Words Not Filtering

**Solution**:
- Check `noise.txt` exists in the project directory
- Verify file encoding is UTF-8
- Ensure no extra spaces around words
- Restart the application after editing `noise.txt`

---

### CSV Export Not Working

**Possible Causes**:
- No analysis has been completed
- Browser blocking download
- Insufficient disk space

**Solutions**:
- Complete an analysis first
- Check browser download settings
- Verify available disk space

---

## Best Practices

### Effective Analysis

1. **Start Small**: Begin with 3-5 pages to get quick results
2. **Be Specific**: Use precise job titles for targeted insights
3. **Multiple Searches**: Run analyses for related roles to identify patterns
4. **Regular Updates**: Analyze periodically to track market trends
5. **Export Data**: Save results for long-term comparison

### Noise Word Management

1. **Review Results**: Check if unwanted words appear frequently
2. **Add to noise.txt**: Include them in the noise word list
3. **Test Again**: Re-run analysis to verify filtering
4. **Keep Updated**: Maintain the noise word list as you discover new patterns
5. **Backup**: Save a copy of your customized `noise.txt`

### Ethical Scraping

1. **Respect Rate Limits**: Don't modify delay times
2. **Reasonable Volume**: Avoid analyzing excessive pages
3. **Personal Use**: Use for research and personal job search
4. **Terms of Service**: Review LinkedIn's terms before use
5. **No Automation**: Run analyses manually, not in automated loops

---

## Contributing

Contributions are welcome! To contribute to Key Finder:

1. Fork the repository at [github.com/humairaambreen/keyfinder](https://github.com/humairaambreen/keyfinder)
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Areas for Contribution

- Additional data sources beyond LinkedIn
- More sophisticated NLP for keyword extraction
- Visualization features (charts, graphs)
- Historical trend tracking
- API for programmatic access
- Alternative UI themes
- Performance optimizations
- Testing suite
- Documentation improvements

---

## License

This project is provided as-is for educational and personal use. Please respect LinkedIn's Terms of Service and use responsibly.

---

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub: [github.com/humairaambreen/keyfinder/issues](https://github.com/humairaambreen/keyfinder/issues)
- Review existing documentation
- Check troubleshooting section

---

**Key Finder** - Discover what skills and keywords matter most in your target job market.
