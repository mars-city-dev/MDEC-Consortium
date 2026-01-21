#!/usr/bin/env python3
"""
MDEC Consortium - Production Server (Port 3000)
Institutionalized Service Wrapper
"""
import logging
import os
import sys

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [MDEC] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('mdec_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

try:
    from flask import Flask, send_from_directory, abort, render_template_string
    from waitress import serve
except ImportError as e:
    logging.critical(f"Missing required package: {e}. Please run: pip install flask waitress")
    sys.exit(1)

app = Flask(__name__)

# Basic MIME type handling for common web assets
import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/markdown', '.md')

@app.route('/health')
def health_check():
    """Service health endpoint for monitoring"""
    return {"status": "active", "service": "MDEC-Consortium", "port": 3000}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    """
    Serve static files with directory fallback.
    If a directory is requested, looks for index.html.
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    if not path:
        path = 'index.html'

    target_path = os.path.join(base_dir, path)

    # Normalize paths for security check (Windows case insensitivity)
    norm_base = os.path.normcase(base_dir)
    norm_target = os.path.normcase(os.path.abspath(target_path))

    # Security check: Prevent directory traversal
    if not norm_target.startswith(norm_base):
        logging.warning(f"Blocked directory traversal attempt: {path}")
        return abort(403)

    # Handle Directories
    if os.path.isdir(target_path):
        index_path = os.path.join(target_path, 'index.html')
        if os.path.exists(index_path):
            # Adjust path to point to the index file
            path = os.path.join(path, 'index.html')
            # target_path is updated for the existence check below? 
            # Actually easiest to just send it now
            # Note: send_from_directory with a relative path (including subdirs) works if base is root
            return send_from_directory(base_dir, path)
            
        else:
            # Simple directory listing
            try:
                files = os.listdir(target_path)
                return render_template_string("""
                    <h1>Directory: {{path}}</h1>
                    <ul>
                    {% for file in files %}
                        <li><a href="{{ file }}">{{ file }}</a></li>
                    {% endfor %}
                    </ul>
                """, path=path, files=files) 
            except Exception as e:
                return abort(404)

    # Handle Files
    if os.path.exists(target_path) and os.path.isfile(target_path):
        return send_from_directory(base_dir, path)
    
    logging.info(f"404 Not Found: {path}")
    return abort(404)

if __name__ == '__main__':
    port = 3000
    logging.info(f"[START] Starting MDEC Consortium Portal on Port {port}")
    logging.info(f"[MODE] Mode: Waitress Production WSGI (Threads: 4)")
    
    try:
        serve(app, host='0.0.0.0', port=port, threads=4, ident="MDEC-Consortium/1.0")
    except Exception as e:
        logging.critical(f"Failed to start server: {e}")
        sys.exit(1)
