#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import subprocess
import threading
import sys
import webbrowser

PORT = 8080

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>SafariBooks Web UI</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f7; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .tabs { display: flex; border-bottom: 2px solid #ddd; margin-bottom: 20px; }
        .tab { padding: 10px 20px; cursor: pointer; border: none; background: none; font-size: 16px; font-weight: bold; color: #555; }
        .tab.active { color: #007aff; border-bottom: 2px solid #007aff; margin-bottom: -2px; }
        .content { display: none; }
        .content.active { display: block; }
        textarea, input[type="text"] { width: 100%; box-sizing: border-box; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; font-family: monospace; }
        button { background: #007aff; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 4px; cursor: pointer; }
        button:hover { background: #005bb5; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        #output { background: #1e1e1e; color: #00ff00; padding: 10px; border-radius: 4px; font-family: monospace; height: 350px; overflow-y: auto; white-space: pre-wrap; margin-top: 20px; font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SafariBooks Downloader</h1>
        <div class="tabs">
            <button class="tab" onclick="showTab('cookies')">1. Paste Cookies</button>
            <button class="tab active" onclick="showTab('download')">2. Download Book</button>
        </div>

        <div id="cookies" class="content">
            <p style="margin-top:0;">Paste your raw <code>cookies.json</code> content below. When you click Save, it will be securely written to the script folder.</p>
            <textarea id="cookies_input" rows="15" placeholder='[{"name": "...", "value": "..."}]'></textarea>
            <button onclick="saveCookies()">Save cookies.json</button>
            <p id="cookies_status"></p>
        </div>

        <div id="download" class="content active">
            <label><b>Book ID or Safari URL:</b></label>
            <input type="text" id="book_id" placeholder="e.g. 9781835880401 or https://learning.oreilly.com/library/view/...">
            <label><input type="checkbox" id="pdf_check" checked> Generate PDF Version</label><br><br>
            <button id="download_btn" onclick="startDownload()">Start Download</button>
            <div id="output">Ready to download...</div>
        </div>
    </div>

    <script>
        function showTab(id) {
            document.querySelectorAll('.tab').forEach((t, i) => t.classList.toggle('active', (id === 'cookies' && i===0) || (id==='download' && i===1)));
            document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
            document.getElementById(id).classList.add('active');
        }

        async function saveCookies() {
            const cookiesText = document.getElementById('cookies_input').value;
            const statusLabel = document.getElementById('cookies_status');
            statusLabel.innerText = "Saving...";
            statusLabel.style.color = "black";

            try {
                const res = await fetch('/save_cookies', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cookies: cookiesText })
                });
                const data = await res.json();
                statusLabel.innerText = data.message;
                statusLabel.style.color = data.status === "success" ? "green" : "red";
                if(data.status === "success") {
                    setTimeout(() => showTab('download'), 1500);
                }
            } catch (err) {
                statusLabel.innerText = 'Error connecting to local server saving cookies.';
                statusLabel.style.color = "red";
            }
        }

        async function startDownload() {
            let bookId = document.getElementById('book_id').value;
            const pdf = document.getElementById('pdf_check').checked;
            const output = document.getElementById('output');
            const btn = document.getElementById('download_btn');
            
            if (!bookId || bookId.trim() === "") {
                alert("Please enter a book ID or URL.");
                return;
            }

            // Extract numeric ID if a full URL was pasted
            bookId = bookId.replace(/\\/$/, '').split('/').pop();

            output.innerHTML = "Starting download for Book ID: " + bookId + "\\n";
            btn.disabled = true;
            btn.innerText = "Downloading...";
            
            try {
                const response = await fetch('/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ book_id: bookId, pdf: pdf })
                });
                
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                async function read() {
                    const { done, value } = await reader.read();
                    if (done) {
                        btn.disabled = false;
                        btn.innerText = "Start Download";
                        return;
                    }
                    output.innerHTML += decoder.decode(value);
                    output.scrollTop = output.scrollHeight; // Auto-scroll
                    read();
                }
                read();
            } catch (err) {
                output.innerHTML += "\\n\\nError communicating with local server: " + err;
                btn.disabled = false;
                btn.innerText = "Start Download";
            }
        }

        // Try to load any existing cookies into textarea on load
        fetch('/load_cookies').then(res => res.json()).then(data => {
            if(data.cookies) {
                document.getElementById('cookies_input').value = data.cookies;
            }
        });
    </script>
</body>
</html>
"""

class WebUIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        elif self.path == '/load_cookies':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = {"cookies": ""}
            if os.path.exists('cookies.json'):
                try:
                    with open('cookies.json', 'r') as f:
                        data["cookies"] = f.read()
                except Exception:
                    pass
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if self.path == '/save_cookies':
            try:
                cookies_json = json.loads(data['cookies'])
                with open('cookies.json', 'w') as f:
                    json.dump(cookies_json, f, indent=4)
                response = {"status": "success", "message": "cookies.json parsed and saved perfectly!"}
            except Exception as e:
                response = {"status": "error", "message": f"Invalid JSON format. Please try copying again!\\nError: {str(e)}"}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path == '/download':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            book_id = data['book_id'].strip('/').split('/')[-1]
            cmd = ['python3', 'safaribooks.py', book_id]
            if data['pdf']:
                cmd.insert(2, '--pdf')

            try:
                # Let's run SafariBooks unbuffered so we get live console stream
                env = os.environ.copy()
                env['PYTHONUNBUFFERED'] = '1'
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, env=env)
                for line in iter(process.stdout.readline, ''):
                    self.wfile.write(line.encode('utf-8'))
                    self.wfile.flush()
                process.stdout.close()
                process.wait()
                self.wfile.write(f"\\nProcess finished! Status code: {process.returncode}\\n".encode('utf-8'))
            except Exception as e:
                self.wfile.write(f"\\nError running script: {str(e)}\\n".encode('utf-8'))

def open_browser():
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    # Find an available port if 8080 is busy
    port = PORT
    while True:
        try:
            httpd = socketserver.ThreadingTCPServer(("", port), WebUIHandler)
            break
        except OSError:
            port += 1

    print(f"\\n---------------------------------------------------------")
    print(f"SafariBooks Web UI started!")
    print(f"Local Server running at: http://localhost:{port}")
    print(f"Keep this terminal open while using the downloader.")
    print(f"Press Control+C here to stop the program when you're done.")
    print(f"---------------------------------------------------------\\n")
    
    # Open the browser immediately
    threading.Timer(0.5, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\nShutting down Local GUI server.")
        httpd.server_close()
        sys.exit(0)
