from flask import Flask, render_template, request, jsonify
import traceback
import numpy as np
import io

from inspiration_engine_phase2 import InspirationEngine
from paper_extractor import extract_systems_from_paper
from system_database_v2 import add_systems_batch, get_database_stats
from neural_ode_learner import learn_ode_from_data, classify_learned_equation

app = Flask(__name__)

engine = InspirationEngine()


@app.route("/", methods=["GET","POST"])
def home():

    result = None
    error = None

    if request.method == "POST":

        try:
            if request.form.get("mode") == "discover":

                result = engine.discovery_mode()

            else:

                subject = request.form.get("subject", "")

                result = engine.solve(subject)

        except Exception as e:
            # Capture the full error
            error = {
                'message': str(e),
                'traceback': traceback.format_exc(),
                'type': type(e).__name__
            }

    return render_template("index.html", result=result, error=error)


@app.route("/extract_paper", methods=["POST"])
def extract_paper():
    """
    Extract systems from a paper abstract
    """

    try:
        abstract = request.form.get("abstract", "")
        title = request.form.get("paper_title", "Untitled")
        authors = request.form.get("authors", "")
        year = request.form.get("year", "")

        if not abstract:
            return jsonify({
                'success': False,
                'error': 'Please provide a paper abstract'
            })

        # Convert year to int if provided
        year_int = None
        if year:
            try:
                year_int = int(year)
            except:
                pass

        # Extract systems
        systems = extract_systems_from_paper(
            text=abstract,
            title=title,
            authors=authors if authors else None,
            year=year_int
        )

        if not systems:
            return jsonify({
                'success': False,
                'error': 'No systems found in this paper. Try a different abstract.'
            })

        # Add to database
        add_systems_batch(systems)

        # Format results
        results = []
        for sys in systems:
            results.append({
                'name': sys.name,
                'domain': sys.domain,
                'mechanisms': sys.mechanisms,
                'citation': sys.get_citation_string()
            })

        return jsonify({
            'success': True,
            'systems_found': len(systems),
            'systems': results
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })


@app.route("/learn_ode", methods=["POST"])
def learn_ode():
    """
    Learn ODE from CSV data
    """

    try:
        csv_data = request.form.get("csv_data", "")

        if not csv_data:
            return jsonify({
                'success': False,
                'error': 'Please provide CSV data (time, value)'
            })

        # Parse CSV data
        lines = csv_data.strip().split('\n')
        time_data = []
        value_data = []

        for line in lines:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                try:
                    time_data.append(float(parts[0].strip()))
                    value_data.append(float(parts[1].strip()))
                except:
                    pass  # Skip bad lines

        if len(time_data) < 3:
            return jsonify({
                'success': False,
                'error': 'Need at least 3 data points. Format: time,value (one per line)'
            })

        # Convert to numpy
        time_array = np.array(time_data)
        value_array = np.array(value_data)

        # Learn ODE
        result = learn_ode_from_data(time_array, value_array, method="polynomial")

        # Classify mechanisms
        mechanisms = classify_learned_equation(
            result['equation'],
            np.array(result['coefficients'])
        )

        return jsonify({
            'success': True,
            'equation': result['equation'],
            'score': result['score'],
            'mechanisms': mechanisms,
            'coefficients': result['coefficients']
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })


@app.route("/database_stats", methods=["GET"])
def database_stats():
    """
    Get database statistics including citations
    """

    try:
        stats = get_database_stats()

        return jsonify({
            'success': True,
            'stats': stats
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route("/fetch_url", methods=["POST"])
def fetch_url():
    """
    Fetch content from a URL and extract systems
    """

    try:
        import requests
        from bs4 import BeautifulSoup

        url = request.form.get("url", "")

        if not url:
            return jsonify({
                'success': False,
                'error': 'Please provide a URL'
            })

        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "Untitled"

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        # Limit to first 5000 characters (roughly an abstract + intro)
        text = text[:5000]

        if len(text) < 100:
            return jsonify({
                'success': False,
                'error': 'Could not extract enough text from URL'
            })

        # Extract systems from the text
        systems = extract_systems_from_paper(
            text=text,
            title=title_text,
            url=url
        )

        if not systems:
            return jsonify({
                'success': False,
                'error': 'No systems found in this page. Try a different URL or paste the text manually.'
            })

        # Add to database
        add_systems_batch(systems)

        # Format results
        results = []
        for sys in systems:
            results.append({
                'name': sys.name,
                'domain': sys.domain,
                'mechanisms': sys.mechanisms,
                'citation': sys.get_citation_string()
            })

        return jsonify({
            'success': True,
            'systems_found': len(systems),
            'systems': results,
            'title': title_text,
            'url': url
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch URL: {str(e)}'
        })

    except ImportError:
        return jsonify({
            'success': False,
            'error': 'Missing dependencies. Install: pip install requests beautifulsoup4'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })


@app.route("/crawl_website", methods=["POST"])
def crawl_website():
    """
    Crawl an entire website and extract systems from all pages
    WITH comprehensive error handling and duplicate prevention
    """

    try:
        import requests
        from bs4 import BeautifulSoup
        from urllib.parse import urljoin, urlparse
        import time

        seed_url = request.form.get("seed_url", "").strip()
        max_pages = int(request.form.get("max_pages", 20))

        if not seed_url:
            return jsonify({
                'success': False,
                'error': 'Please provide a seed URL'
            })

        # Parse seed URL to get domain
        parsed_seed = urlparse(seed_url)
        seed_domain = parsed_seed.netloc

        # Track visited and to-visit URLs
        visited = set()
        to_visit = {seed_url}
        all_systems = []
        pages_processed = 0

        # Track errors and stats
        errors = {
            '404': 0,
            '403': 0,
            '500': 0,
            'timeout': 0,
            'connection': 0,
            'other': 0
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # Get existing systems to check for duplicates
        from system_database_v2 import load_systems
        existing_systems = load_systems()
        existing_names = {s.name.lower().strip() for s in existing_systems}

        while to_visit and pages_processed < max_pages:
            # Get next URL
            current_url = to_visit.pop()

            # Skip if already visited
            if current_url in visited:
                continue

            visited.add(current_url)
            pages_processed += 1

            try:
                # Fetch page with timeout
                response = requests.get(current_url, headers=headers, timeout=10)

                # Check HTTP status
                if response.status_code == 404:
                    errors['404'] += 1
                    continue
                elif response.status_code == 403:
                    errors['403'] += 1
                    continue
                elif response.status_code >= 500:
                    errors['500'] += 1
                    continue

                # Raise for other bad status codes
                response.raise_for_status()

                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract title
                title = soup.find('title')
                title_text = title.get_text().strip() if title else f"Page {pages_processed}"

                # Remove junk
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()

                # Get text
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                text = text[:5000]

                # Extract systems from this page
                if len(text) >= 100:
                    page_systems = extract_systems_from_paper(
                        text=text,
                        title=title_text,
                        url=current_url
                    )

                    # Filter out duplicates
                    if page_systems:
                        for sys in page_systems:
                            # Check if system name already exists (case-insensitive)
                            sys_name_lower = sys.name.lower().strip()
                            if sys_name_lower not in existing_names:
                                all_systems.append(sys)
                                existing_names.add(sys_name_lower)  # Track to avoid duplicates within this crawl too

                # Find all links on this page
                for link in soup.find_all('a', href=True):
                    href = link['href']

                    # Convert relative URLs to absolute
                    absolute_url = urljoin(current_url, href)

                    # Only crawl same domain
                    parsed_url = urlparse(absolute_url)
                    if parsed_url.netloc == seed_domain:
                        # Remove fragments (#)
                        clean_url = absolute_url.split('#')[0]
                        # Skip already visited
                        if clean_url not in visited:
                            to_visit.add(clean_url)

                # Rate limiting - be respectful!
                time.sleep(0.5)

            except requests.exceptions.Timeout:
                errors['timeout'] += 1
                continue

            except requests.exceptions.ConnectionError:
                errors['connection'] += 1
                continue

            except requests.exceptions.HTTPError as e:
                if '404' in str(e):
                    errors['404'] += 1
                elif '403' in str(e):
                    errors['403'] += 1
                elif '500' in str(e) or '502' in str(e) or '503' in str(e):
                    errors['500'] += 1
                else:
                    errors['other'] += 1
                continue

            except Exception as e:
                # Catch any other errors
                errors['other'] += 1
                continue

        # Add all NEW systems to database
        new_count = 0
        if all_systems:
            add_systems_batch(all_systems)
            new_count = len(all_systems)

        # Calculate total errors
        total_errors = sum(errors.values())

        # Format results
        results = []
        for sys in all_systems:
            results.append({
                'name': sys.name,
                'domain': sys.domain,
                'mechanisms': sys.mechanisms,
                'citation': sys.get_citation_string()
            })

        return jsonify({
            'success': True,
            'pages_crawled': pages_processed,
            'pages_successful': pages_processed - total_errors,
            'pages_errored': total_errors,
            'errors': errors,
            'systems_found': new_count,
            'systems_skipped_duplicates': len(existing_systems) if new_count == 0 else 0,
            'systems': results
        })

    except ImportError:
        return jsonify({
            'success': False,
            'error': 'Missing dependencies. Install: pip install requests beautifulsoup4'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })


@app.route("/crawl_website_stream", methods=["POST"])
def crawl_website_stream():
    """
    Crawl website with live progress updates via Server-Sent Events (SSE)
    """

    # Get parameters BEFORE entering generator (in request context!)
    seed_url = request.form.get("seed_url", "").strip()
    max_pages_str = request.form.get("max_pages", "20")

    def generate(seed_url, max_pages_str):
        try:
            import requests
            from bs4 import BeautifulSoup
            from urllib.parse import urljoin, urlparse
            import time
            import json

            # Handle "unlimited" option
            if max_pages_str == "unlimited":
                max_pages = float('inf')  # No limit!
            else:
                max_pages = int(max_pages_str)

            if not seed_url:
                yield f"data: {json.dumps({'error': 'Please provide a seed URL'})}\n\n"
                return

            # Send initial status
            yield f"data: {json.dumps({'status': 'starting', 'seed_url': seed_url, 'max_pages': max_pages_str})}\n\n"

            parsed_seed = urlparse(seed_url)
            seed_domain = parsed_seed.netloc

            visited = set()
            to_visit = {seed_url}
            all_systems = []
            pages_processed = 0

            errors = {
                '404': 0,
                '403': 0,
                '500': 0,
                'timeout': 0,
                'connection': 0,
                'other': 0
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            from system_database_v2 import load_systems
            existing_systems = load_systems()
            existing_names = {s.name.lower().strip() for s in existing_systems}

            while to_visit and pages_processed < max_pages:
                current_url = to_visit.pop()

                if current_url in visited:
                    continue

                visited.add(current_url)
                pages_processed += 1

                # Send progress update
                progress = {
                    'status': 'crawling',
                    'current_page': pages_processed,
                    'max_pages': max_pages_str,
                    'url': current_url,
                    'systems_found': len(all_systems),
                    'pages_remaining': len(to_visit),
                    'errors': errors
                }
                yield f"data: {json.dumps(progress)}\n\n"

                try:
                    response = requests.get(current_url, headers=headers, timeout=10)

                    if response.status_code == 404:
                        errors['404'] += 1
                        continue
                    elif response.status_code == 403:
                        errors['403'] += 1
                        continue
                    elif response.status_code >= 500:
                        errors['500'] += 1
                        continue

                    response.raise_for_status()

                    soup = BeautifulSoup(response.text, 'html.parser')

                    title = soup.find('title')
                    title_text = title.get_text().strip() if title else f"Page {pages_processed}"

                    for script in soup(["script", "style", "nav", "footer", "header"]):
                        script.decompose()

                    text = soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    text = text[:5000]

                    if len(text) >= 100:
                        page_systems = extract_systems_from_paper(
                            text=text,
                            title=title_text,
                            url=current_url
                        )

                        if page_systems:
                            for sys in page_systems:
                                sys_name_lower = sys.name.lower().strip()
                                if sys_name_lower not in existing_names:
                                    all_systems.append(sys)
                                    existing_names.add(sys_name_lower)

                                    # Send update about new system found
                                    yield f"data: {json.dumps({{'status': 'system_found', 'system_name': sys.name, 'domain': sys.domain}})}\n\n"

                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        absolute_url = urljoin(current_url, href)
                        parsed_url = urlparse(absolute_url)

                        if parsed_url.netloc == seed_domain:
                            clean_url = absolute_url.split('#')[0]
                            if clean_url not in visited:
                                to_visit.add(clean_url)

                    time.sleep(0.5)

                except requests.exceptions.Timeout:
                    errors['timeout'] += 1
                    continue
                except requests.exceptions.ConnectionError:
                    errors['connection'] += 1
                    continue
                except requests.exceptions.HTTPError as e:
                    if '404' in str(e):
                        errors['404'] += 1
                    elif '403' in str(e):
                        errors['403'] += 1
                    elif '500' in str(e) or '502' in str(e) or '503' in str(e):
                        errors['500'] += 1
                    else:
                        errors['other'] += 1
                    continue
                except Exception as e:
                    errors['other'] += 1
                    continue

            # Add systems to database
            new_count = 0
            if all_systems:
                add_systems_batch(all_systems)
                new_count = len(all_systems)

            # Send completion
            total_errors = sum(errors.values())

            results = []
            for sys in all_systems:
                results.append({
                    'name': sys.name,
                    'domain': sys.domain,
                    'mechanisms': sys.mechanisms,
                    'citation': sys.get_citation_string()
                })

            final_data = {
                'status': 'complete',
                'pages_crawled': pages_processed,
                'pages_successful': pages_processed - total_errors,
                'pages_errored': total_errors,
                'errors': errors,
                'systems_found': new_count,
                'systems': results
            }

            yield f"data: {json.dumps(final_data)}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'error': str(e)})}\n\n"

    # Call generator with parameters
    return app.response_class(generate(seed_url, max_pages_str), mimetype='text/event-stream')


app.run(host="0.0.0.0", port=5000)
