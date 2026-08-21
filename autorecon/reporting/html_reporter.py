import os
import datetime
import jinja2
from autorecon.core.config import OUTPUT_DIR

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoRecon Studio - Reconnaissance Report</title>
    <style>
        :root {
            --bg-color: #0f1117;
            --card-bg: #1e2230;
            --text-primary: #f5f5f7;
            --text-secondary: #86868b;
            --border-color: rgba(255, 255, 255, 0.08);
            --accent-blue: #0A84FF;
            --accent-green: #30D158;
            --accent-red: #FF453A;
            --font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-primary);
            font-family: var(--font-family);
            margin: 0;
            padding: 20px;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
            padding: 20px 0;
            border-bottom: 1px solid var(--border-color);
        }

        h1 {
            font-size: 32px;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .meta {
            color: var(--text-secondary);
            font-size: 14px;
            margin-top: 10px;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .summary-card {
            background-color: var(--card-bg);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
            text-align: center;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        }

        .summary-card h3 {
            margin: 0;
            font-size: 14px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .summary-card .value {
            font-size: 36px;
            font-weight: 700;
            margin-top: 10px;
            color: var(--accent-blue);
        }

        .module-card {
            background-color: var(--card-bg);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }

        .module-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
        }

        .module-header h2 {
            margin: 0;
            font-size: 20px;
            font-weight: 600;
        }

        .badge {
            background-color: rgba(10, 132, 255, 0.15);
            color: var(--accent-blue);
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }

        pre {
            background-color: rgba(0, 0, 0, 0.3);
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 13px;
            color: #d4d4d4;
            border: 1px solid var(--border-color);
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .empty-state {
            text-align: center;
            color: var(--text-secondary);
            font-style: italic;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>AutoRecon Studio Report</h1>
            <div class="meta">Target: <strong>{{ target }}</strong> &nbsp;|&nbsp; Generated: {{ timestamp }}</div>
        </header>

        <div class="summary-grid">
            <div class="summary-card">
                <h3>Target</h3>
                <div class="value" style="font-size: 24px; line-height: 1.5;">{{ target }}</div>
            </div>
            <div class="summary-card">
                <h3>Modules Run</h3>
                <div class="value">{{ results|length }}</div>
            </div>
            <div class="summary-card">
                <h3>Total Time</h3>
                <div class="value">~{{ duration }}s</div>
            </div>
        </div>

        {% for module_name, output in results.items() %}
        <div class="module-card">
            <div class="module-header">
                <h2>{{ module_name }}</h2>
                <span class="badge">Completed</span>
            </div>
            {% if output %}
            <pre><code>{{ output | e }}</code></pre>
            {% else %}
            <div class="empty-state">No output generated by this module.</div>
            {% endif %}
        </div>
        {% endfor %}
        
        {% if not results %}
        <div class="module-card">
            <div class="empty-state">No modules were run or no results were recorded.</div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def generate_html_report(target: str, results: dict, duration: int) -> str:
    """Generates an HTML report and saves it to the output directory."""
    template = jinja2.Template(HTML_TEMPLATE)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = template.render(
        target=target,
        timestamp=timestamp,
        results=results,
        duration=duration
    )
    
    safe_target = target.replace(".", "_").replace(":", "_").replace("/", "_")
    filename = f"autorecon_{safe_target}_{int(datetime.datetime.now().timestamp())}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    return filepath
