#!/usr/bin/env python3
"""
Development server with auto-reload functionality for HTML files.
Serves static files and automatically refreshes the browser when files change.
"""

import os
import sys
import time
import asyncio
import threading
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import webbrowser
from urllib.parse import urlparse

class AutoReloadHandler(FileSystemEventHandler):
    """Handler for file system events that triggers browser refresh."""
    
    def __init__(self, websocket_clients):
        self.websocket_clients = websocket_clients
        self.last_reload = 0
        
    def on_modified(self, event):
        """Called when a file is modified."""
        if event.is_directory:
            return
            
        # Debounce rapid file changes
        current_time = time.time()
        if current_time - self.last_reload < 0.5:  # 500ms debounce
            return
        self.last_reload = current_time
        
        # Check if it's a relevant file type
        file_path = event.src_path
        relevant_extensions = {'.html', '.css', '.js', '.htm', '.xml', '.json'}
        if any(file_path.endswith(ext) for ext in relevant_extensions):
            print(f"📝 File changed: {file_path}")
            self.trigger_reload()
    
    def trigger_reload(self):
        """Trigger browser reload via WebSocket or inject script."""
        print("🔄 Triggering page reload...")
        # In a simple setup, we'll use the injection method

class ReloadableHTTPRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler that injects auto-reload script into HTML pages."""
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def do_GET(self):
        """Override GET to inject reload script into HTML files."""
        # Get the file path
        path = self.translate_path(self.path)
        
        if os.path.isfile(path) and path.endswith(('.html', '.htm')):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Inject auto-reload script before closing </body> tag
                reload_script = '''
<script>
(function() {
    let lastModified = Date.now();
    
    function checkForUpdates() {
        fetch(window.location.href, {
            method: 'HEAD',
            cache: 'no-cache'
        }).then(response => {
            const modified = new Date(response.headers.get('Last-Modified')).getTime();
            if (modified > lastModified) {
                console.log('🔄 Reloading page due to file changes...');
                window.location.reload();
            }
        }).catch(() => {
            // Ignore errors, server might be restarting
        });
    }
    
    // Check for updates every 1 second
    setInterval(checkForUpdates, 1000);
    
    // Also listen for focus events (when user switches back to tab)
    window.addEventListener('focus', checkForUpdates);
    
    console.log('🚀 Auto-reload enabled - page will refresh when files change');
})();
</script>
'''
                
                # Insert script before closing body tag, or before closing html tag if no body
                if '</body>' in content:
                    content = content.replace('</body>', reload_script + '\n</body>')
                elif '</html>' in content:
                    content = content.replace('</html>', reload_script + '\n</html>')
                else:
                    content += reload_script
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content.encode('utf-8'))))
                self.send_header('Last-Modified', self.date_time_string(os.path.getmtime(path)))
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                return
            except Exception as e:
                print(f"Error processing HTML file: {e}")
        
        # For all other files, use default behavior
        super().do_GET()

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """Threaded HTTP server for better performance."""
    daemon_threads = True

def start_file_watcher(directory, websocket_clients):
    """Start watching files for changes."""
    event_handler = AutoReloadHandler(websocket_clients)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    print(f"👀 Watching for file changes in: {directory}")
    return observer

def main():
    """Main function to start the development server."""
    # Parse command line arguments
    port = 8080
    directory = "."
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            directory = sys.argv[1]
            if len(sys.argv) > 2:
                try:
                    port = int(sys.argv[2])
                except ValueError:
                    pass
    
    # Change to the specified directory
    os.chdir(directory)
    current_dir = os.getcwd()
    
    print("🚀 Starting Auto-Reload Development Server")
    print(f"📁 Serving directory: {current_dir}")
    print(f"🌐 Server running at: http://localhost:{port}")
    print("🔄 Auto-reload enabled - pages will refresh when files change")
    print("⏹️  Press Ctrl+C to stop the server")
    
    # WebSocket clients (for future enhancement)
    websocket_clients = set()
    
    # Start file watcher
    observer = start_file_watcher(current_dir, websocket_clients)
    
    try:
        # Start HTTP server
        httpd = ThreadingHTTPServer(("", port), ReloadableHTTPRequestHandler)
        
        # Open browser
        server_url = f"http://localhost:{port}"
        threading.Timer(1.0, lambda: webbrowser.open(server_url)).start()
        
        # Run server
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        observer.stop()
        observer.join()
        httpd.shutdown()
        print("✅ Server stopped")

if __name__ == "__main__":
    main()
