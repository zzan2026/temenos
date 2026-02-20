#!/usr/bin/env python3
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


def get_temenos_stock():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/TEMN.SW"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            meta = data["chart"]["result"][0]["meta"]
            price = meta["regularMarketPrice"]
            currency = meta["currency"]
            return f"{price:.2f} {currency}"
    except Exception as e:
        return f"N/A ({e})"


class TemenosHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        stock_price = get_temenos_stock()
        current_date = datetime.now().strftime("%A, %B %d, %Y — %H:%M:%S")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Temenos</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #0d1b2a 0%, #1b2f4e 50%, #0d1b2a 100%);
      color: #fff;
    }}
    .card {{
      text-align: center;
      padding: 60px 80px;
      background: rgba(255, 255, 255, 0.07);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 20px;
      backdrop-filter: blur(12px);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
      max-width: 600px;
      width: 90%;
    }}
    .logo {{
      font-size: 0.9em;
      letter-spacing: 0.35em;
      text-transform: uppercase;
      color: #7ec8e3;
      margin-bottom: 24px;
    }}
    h1 {{
      font-size: 2.8em;
      font-weight: 700;
      margin-bottom: 30px;
      background: linear-gradient(90deg, #7ec8e3, #ffffff, #a8d8ea);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}
    .date {{
      font-size: 1.05em;
      color: #aac4d8;
      margin-bottom: 28px;
      letter-spacing: 0.03em;
    }}
    .stock-box {{
      display: inline-block;
      background: rgba(126, 200, 227, 0.12);
      border: 1px solid rgba(126, 200, 227, 0.35);
      border-radius: 10px;
      padding: 14px 32px;
    }}
    .stock-label {{
      font-size: 0.8em;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: #7ec8e3;
      margin-bottom: 6px;
    }}
    .stock-price {{
      font-size: 2em;
      font-weight: 600;
      color: #58d68d;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">Temenos</div>
    <h1>Hello Temenos World</h1>
    <div class="date">{current_date}</div>
    <div class="stock-box">
      <div class="stock-label">TEMN.SW</div>
      <div class="stock-price">{stock_price}</div>
    </div>
  </div>
</body>
</html>"""

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, format, *args):
        print(f"  {self.address_string()} - {args[0]}")


if __name__ == "__main__":
    port = 4867
    server = HTTPServer(("0.0.0.0", port), TemenosHandler)
    print(f"Temenos server running at http://localhost:{port}")
    server.serve_forever()
