from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict
import re
from urllib.parse import quote_plus
import time
from threading import Thread
import os

app = Flask(__name__)
CORS(app)

# Global variable to store analysis progress
analysis_progress = {
    'status': 'idle',
    'current_page': 0,
    'total_pages': 0,
    'jobs_found': 0,
    'current_job': '',
    'results': None,
    'error': None
}

class KeyFinder:
    def __init__(self):
        self.keyword_jobs = defaultdict(set)
        self.all_jobs = []
        self.noise_words = self.load_noise_words()
    
    def load_noise_words(self):
        """Load noise words from noise.txt file"""
        noise_words = set()
        noise_file = 'noise.txt'
        
        try:
            if os.path.exists(noise_file):
                with open(noise_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Skip only empty lines
                        if line:
                            # Handle comma-separated values on the same line
                            if ',' in line:
                                words = [w.strip().lower() for w in line.split(',') if w.strip()]
                                noise_words.update(words)
                            else:
                                noise_words.add(line.lower())
                print(f"✓ Loaded {len(noise_words)} noise words from {noise_file}")
            else:
                print(f"⚠ Warning: {noise_file} not found. Using empty noise words set.")
        except Exception as e:
            print(f"⚠ Error loading noise words: {e}")
        
        return noise_words
    
    def fetch_job_description(self, url, headers):
        try:
            time.sleep(1)
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            desc = (soup.find('div', class_='description__text') or
                   soup.find('div', class_='show-more-less-html__markup') or
                   soup.find('section', class_='description'))
            if desc:
                return desc.get_text(separator=' ', strip=True)
        except:
            pass
        return ''
    
    def extract_keywords(self, text):
        if not text:
            return set()
        text = text.lower()
        text = re.sub(r'[^\w\s\+\#\.]', ' ', text)
        words = text.split()
        keywords = set()
        
        for word in words:
            word = word.strip()
            if (len(word) >= 2 and len(word) <= 50 and
                word not in self.noise_words and not word.isdigit()):
                keywords.add(word)
        
        for i in range(len(words) - 1):
            if (words[i] not in self.noise_words and words[i+1] not in self.noise_words):
                phrase = f"{words[i]} {words[i+1]}"
                if len(phrase) <= 50 and phrase not in self.noise_words:
                    keywords.add(phrase)
        
        for i in range(len(words) - 2):
            if (words[i] not in self.noise_words and 
                words[i+1] not in self.noise_words and
                words[i+2] not in self.noise_words):
                phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
                if len(phrase) <= 50 and phrase not in self.noise_words:
                    keywords.add(phrase)
        
        return keywords
    
    def analyze(self, keyword, num_pages=5, progress_callback=None):
        if progress_callback:
            progress_callback('running', 0, num_pages, 0, f'Starting search for: {keyword}')
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        for page in range(num_pages):
            if progress_callback:
                progress_callback('running', page + 1, num_pages, len(self.all_jobs), 
                                f'Scraping page {page+1}/{num_pages}...')
            
            try:
                start = page * 25
                url = f"https://www.linkedin.com/jobs/search?keywords={quote_plus(keyword)}&start={start}"
                response = requests.get(url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                job_cards = (soup.find_all('div', class_='base-card') or
                            soup.find_all('div', class_='job-search-card'))
                
                for card in job_cards:
                    try:
                        link = card.find('a', href=re.compile(r'/jobs/view/'))
                        if not link:
                            continue
                        
                        job_url = link['href']
                        if not job_url.startswith('http'):
                            job_url = f"https://www.linkedin.com{job_url.split('?')[0]}"
                        else:
                            job_url = job_url.split('?')[0]
                        
                        title_elem = card.find('h3')
                        title = title_elem.get_text(strip=True) if title_elem else ''
                        
                        description = self.fetch_job_description(job_url, headers)
                        
                        if description:
                            keywords = self.extract_keywords(description)
                            job_index = len(self.all_jobs)
                            
                            for kw in keywords:
                                self.keyword_jobs[kw].add(job_index)
                            
                            self.all_jobs.append({
                                'title': title,
                                'url': job_url,
                                'description': description
                            })
                            
                            if progress_callback:
                                progress_callback('running', page + 1, num_pages, len(self.all_jobs), 
                                                f'Found: {title[:60]}')
                    except:
                        continue
                
                time.sleep(2)
            except:
                if progress_callback:
                    progress_callback('running', page + 1, num_pages, len(self.all_jobs), 
                                    f'Page {page+1} failed, continuing...')
        
        if progress_callback:
            progress_callback('completed', num_pages, num_pages, len(self.all_jobs), 
                            f'Analysis complete! Analyzed {len(self.all_jobs)} jobs')
        
        return self.get_results(keyword)
    
    def get_results(self, keyword):
        keyword_stats = {}
        total_jobs = len(self.all_jobs)
        
        for kw, job_set in self.keyword_jobs.items():
            num_jobs = len(job_set)
            if num_jobs >= 2:
                percentage = (num_jobs / total_jobs) * 100
                keyword_stats[kw] = {
                    'count': num_jobs,
                    'percentage': percentage
                }
        
        sorted_keywords = dict(sorted(
            keyword_stats.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        ))
        
        return {
            'keyword': keyword,
            'total_jobs': total_jobs,
            'keywords': sorted_keywords,
            'jobs': self.all_jobs
        }
    
    def export_results(self, results):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        keywords_file = f"keywords_{results['keyword'].replace(' ', '_')}_{timestamp}.csv"
        df = pd.DataFrame([
            {'Rank': i, 'Keyword': kw, 'Jobs': s['count'], 'Percentage': f"{s['percentage']:.1f}%"}
            for i, (kw, s) in enumerate(results['keywords'].items(), 1)
        ])
        df.to_csv(keywords_file, index=False)
        print(f"✓ Saved: {keywords_file}")
        
        jobs_file = f"jobs_{results['keyword'].replace(' ', '_')}_{timestamp}.csv"
        jobs_df = pd.DataFrame([
            {'Title': j['title'], 'URL': j['url'], 'Description': j['description'][:500]}
            for j in results['jobs']
        ])
        jobs_df.to_csv(jobs_file, index=False)
        print(f"✓ Saved: {jobs_file}")


def update_progress(status, current_page, total_pages, jobs_found, message):
    global analysis_progress
    analysis_progress['status'] = status
    analysis_progress['current_page'] = current_page
    analysis_progress['total_pages'] = total_pages
    analysis_progress['jobs_found'] = jobs_found
    analysis_progress['current_job'] = message


def run_analysis(keyword, num_pages):
    global analysis_progress
    try:
        analyzer = KeyFinder()
        results = analyzer.analyze(keyword, num_pages, progress_callback=update_progress)
        analysis_progress['results'] = results
        analysis_progress['status'] = 'completed'
    except Exception as e:
        analysis_progress['status'] = 'error'
        analysis_progress['error'] = str(e)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    global analysis_progress
    
    data = request.json
    keyword = data.get('keyword', '').strip()
    num_pages = int(data.get('pages', 5))
    
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400
    
    # Reset progress
    analysis_progress = {
        'status': 'starting',
        'current_page': 0,
        'total_pages': num_pages,
        'jobs_found': 0,
        'current_job': '',
        'results': None,
        'error': None
    }
    
    # Run analysis in background thread
    thread = Thread(target=run_analysis, args=(keyword, num_pages))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started'})


@app.route('/progress')
def progress():
    global analysis_progress
    return jsonify(analysis_progress)


@app.route('/export/<file_type>')
def export(file_type):
    global analysis_progress
    
    if not analysis_progress.get('results'):
        return jsonify({'error': 'No results to export'}), 400
    
    results = analysis_progress['results']
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    if file_type == 'keywords':
        filename = f"keywords_{results['keyword'].replace(' ', '_')}_{timestamp}.csv"
        df = pd.DataFrame([
            {'Rank': i, 'Keyword': kw, 'Jobs': s['count'], 'Percentage': f"{s['percentage']:.1f}%"}
            for i, (kw, s) in enumerate(results['keywords'].items(), 1)
        ])
        df.to_csv(filename, index=False)
        return send_file(filename, as_attachment=True)
    
    elif file_type == 'jobs':
        filename = f"jobs_{results['keyword'].replace(' ', '_')}_{timestamp}.csv"
        jobs_df = pd.DataFrame([
            {'Title': j['title'], 'URL': j['url'], 'Description': j['description'][:500]}
            for j in results['jobs']
        ])
        jobs_df.to_csv(filename, index=False)
        return send_file(filename, as_attachment=True)
    
    return jsonify({'error': 'Invalid file type'}), 400


if __name__ == "__main__":
    print("\n" + "=" * 100)
    print("KEY FINDER - LINKEDIN JOB KEYWORD ANALYSIS TOOL")
    print("=" * 100)
    print("\nStarting web server...")
    print("Open your browser and go to: http://localhost:5001")
    print("\n" + "=" * 100 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5001)