import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

def build_template(dynamic_title: str) -> str:
    """
    Constructs the enterprise dashboard template.
    Interpolates dynamic_title directly via f-string to demonstrate the SSTI vulnerability point.
    """
    return f"""<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SysHealth Enterprise Portal</title>
    <!-- Bootstrap 5.3 CSS CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons CDN -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <style>
        :root {{
            --bg-main: #0f172a;
            --card-bg: #1e293b;
            --border-color: #334155;
            --border-focus: #38bdf8;
            --terminal-bg: #090d16;
            --text-muted-custom: #94a3b8;
        }}
        body {{
            background-color: var(--bg-main);
            color: #f1f5f9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            min-height: 100vh;
        }}
        .navbar-custom {{
            background-color: #0b1120;
            border-bottom: 1px solid var(--border-color);
        }}
        .card-custom {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
        }}
        .status-dot {{
            width: 8px;
            height: 8px;
            background-color: #10b981;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px #10b981;
            animation: pulse-dot 2s infinite ease-in-out;
        }}
        @keyframes pulse-dot {{
            0%, 100% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.3); opacity: 0.6; }}
        }}
        .terminal-window {{
            background-color: var(--terminal-bg);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            overflow: hidden;
        }}
        .terminal-header {{
            background-color: #141c2e;
            padding: 8px 14px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .terminal-dots {{
            display: flex;
            gap: 6px;
        }}
        .dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
        }}
        .dot-red {{ background-color: #ef4444; }}
        .dot-yellow {{ background-color: #f59e0b; }}
        .dot-green {{ background-color: #10b981; }}
        pre.terminal-content {{
            margin: 0;
            padding: 1rem;
            color: #38bdf8;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 0.875rem;
            white-space: pre-wrap;
            word-break: break-all;
            max-height: 280px;
            overflow-y: auto;
        }}
        .metric-badge {{
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
        }}
        .form-control, .form-control:focus {{
            background-color: #0f172a;
            border-color: var(--border-color);
            color: #f8fafc;
        }}
        .form-control:focus {{
            border-color: var(--border-focus);
            box-shadow: 0 0 0 0.25rem rgba(56, 189, 248, 0.2);
        }}
        .input-group-text {{
            background-color: #141e33;
            border-color: var(--border-color);
            color: var(--text-muted-custom);
        }}
        .service-row {{
            border-bottom: 1px solid rgba(51, 65, 85, 0.4);
            padding: 0.6rem 0;
        }}
        .service-row:last-child {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <!-- Enterprise Navbar -->
    <nav class="navbar navbar-custom navbar-expand-lg px-4 py-3">
        <div class="container-fluid">
            <div class="d-flex align-items-center gap-3">
                <div class="d-flex align-items-center justify-content-center bg-primary bg-opacity-10 border border-primary border-opacity-25 rounded-3 p-2 text-info">
                    <i class="bi bi-shield-check fs-5"></i>
                </div>
                <div>
                    <span class="fs-5 fw-bold text-white tracking-wide">SysHealth</span>
                    <span class="badge bg-secondary-subtle text-light border border-secondary border-opacity-25 ms-1 px-2 py-1 small">Enterprise Portal</span>
                    <div class="text-secondary small font-monospace" style="font-size: 0.75rem;">NODE: cluster-prod-01</div>
                </div>
            </div>

            <div class="d-flex align-items-center gap-3 mt-2 mt-lg-0">
                <div class="d-flex align-items-center gap-2 px-3 py-1 rounded-pill" style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35);">
                    <span class="status-dot"></span>
                    <span class="text-success fw-semibold small">Operational</span>
                </div>
                <div class="d-none d-md-flex align-items-center gap-3 text-secondary small border-start border-secondary border-opacity-25 ps-3 font-monospace">
                    <span><i class="bi bi-hdd-network me-1 text-info"></i> gateway: 10.10.0.1</span>
                    <span><i class="bi bi-stopwatch me-1 text-warning"></i> latency: 8ms</span>
                    <span><i class="bi bi-check2-circle me-1 text-success"></i> SLA: 99.98%</span>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Dashboard Container -->
    <div class="container-fluid px-4 py-4">

        <!-- Top Telemetry Row -->
        <div class="row g-3 mb-4">
            <div class="col-6 col-md-3">
                <div class="metric-badge">
                    <div class="text-secondary small mb-1"><i class="bi bi-cpu text-info me-1"></i> CPU Allocation</div>
                    <div class="fs-5 fw-bold text-white">12.8% <span class="badge bg-success-subtle text-success small fw-normal ms-1">Nominal</span></div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="metric-badge">
                    <div class="text-secondary small mb-1"><i class="bi bi-memory text-warning me-1"></i> Memory Pool</div>
                    <div class="fs-5 fw-bold text-white">3.2 GB <span class="text-secondary small fw-normal">/ 16 GB</span></div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="metric-badge">
                    <div class="text-secondary small mb-1"><i class="bi bi-boxes text-primary me-1"></i> Mesh Services</div>
                    <div class="fs-5 fw-bold text-white">16 / 16 <span class="badge bg-primary-subtle text-primary small fw-normal ms-1">Active</span></div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="metric-badge">
                    <div class="text-secondary small mb-1"><i class="bi bi-shield-lock text-success me-1"></i> Security Filter</div>
                    <div class="fs-5 fw-bold text-success">Enforced <i class="bi bi-patch-check-fill ms-1"></i></div>
                </div>
            </div>
        </div>

        <!-- 2-Column Core Layout -->
        <div class="row g-4">

            <!-- Left Column: Feature 1 (SSTI Stage) -->
            <div class="col-lg-6">
                <div class="card card-custom h-100 p-4">
                    <div class="d-flex align-items-start justify-content-between mb-3">
                        <div>
                            <span class="badge bg-primary-subtle text-primary border border-primary border-opacity-25 mb-2">Stage 01: Header Customization</span>
                            <!-- DYNAMIC RENDERED TITLE (SSTI SINK) -->
                            <h3 class="fw-bold text-white mb-1" id="section-title">{dynamic_title}</h3>
                            <p class="text-secondary small mb-0">Customizable summary banner via GET parameter <code>title</code>.</p>
                        </div>
                        <div class="bg-primary bg-opacity-10 text-primary p-2 rounded-3">
                            <i class="bi bi-layout-text-window-reverse fs-4"></i>
                        </div>
                    </div>

                    {{% if ssti_warning %}}
                    <div class="alert alert-warning border-warning border-opacity-50 d-flex align-items-center py-2 px-3 mb-3" role="alert">
                        <i class="bi bi-exclamation-triangle-fill fs-5 text-warning me-2 flex-shrink-0"></i>
                        <div class="small fw-semibold text-warning-emphasis">
                            {{{{ ssti_warning }}}}
                        </div>
                    </div>
                    {{% endif %}}

                    <!-- Title Customization Form (GET) -->
                    <form method="GET" action="/" class="mb-4">
                        <label for="title" class="form-label text-secondary small fw-semibold">Workspace Header Parameter</label>
                        <div class="input-group">
                            <span class="input-group-text"><i class="bi bi-pencil-square"></i></span>
                            <input type="text" class="form-control" id="title" name="title" value="{{{{ current_title }}}}" placeholder="e.g. System Health Summary">
                            <button class="btn btn-primary px-3 fw-semibold" type="submit">
                                <i class="bi bi-arrow-repeat me-1"></i> Update Header
                            </button>
                        </div>
                        <div class="form-text text-secondary small mt-1">
                            Active Query: <code class="text-info">?title={{{{ current_title }}}}</code>
                        </div>
                    </form>

                    <!-- System Telemetry Table -->
                    <div class="mt-auto">
                        <h6 class="text-white-50 small fw-bold text-uppercase tracking-wider mb-2">Internal Service Mesh</h6>
                        <div class="bg-dark bg-opacity-50 rounded-3 p-3 border border-secondary border-opacity-25">
                            <div class="d-flex justify-content-between align-items-center service-row">
                                <div class="d-flex align-items-center gap-2">
                                    <i class="bi bi-diagram-3 text-info"></i>
                                    <span class="small text-white">auth.gateway.internal</span>
                                </div>
                                <span class="badge bg-success-subtle text-success small">RUNNING</span>
                            </div>
                            <div class="d-flex justify-content-between align-items-center service-row">
                                <div class="d-flex align-items-center gap-2">
                                    <i class="bi bi-database-check text-warning"></i>
                                    <span class="small text-white">cluster-telemetry-broker</span>
                                </div>
                                <span class="badge bg-success-subtle text-success small">HEALTHY</span>
                            </div>
                            <div class="d-flex justify-content-between align-items-center service-row">
                                <div class="d-flex align-items-center gap-2">
                                    <i class="bi bi-cpu text-primary"></i>
                                    <span class="small text-white">kernel-health-daemon</span>
                                </div>
                                <span class="badge bg-success-subtle text-success small">ONLINE</span>
                            </div>
                            <div class="d-flex justify-content-between align-items-center service-row">
                                <div class="d-flex align-items-center gap-2">
                                    <i class="bi bi-shield-shaded text-danger"></i>
                                    <span class="small text-white">sentinel-waf-layer</span>
                                </div>
                                <span class="badge bg-info-subtle text-info small">FILTER ACTIVE</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Column: Feature 2 (Command Injection Stage) -->
            <div class="col-lg-6">
                <div class="card card-custom h-100 p-4">
                    <div class="d-flex align-items-start justify-content-between mb-3">
                        <div>
                            <span class="badge bg-info-subtle text-info border border-info border-opacity-25 mb-2">Stage 02: Network Reachability Probe</span>
                            <h3 class="fw-bold text-white mb-1">ICMP Ping Diagnostics</h3>
                            <p class="text-secondary small mb-0">Evaluate round-trip latency and node connectivity across cluster nodes.</p>
                        </div>
                        <div class="bg-info bg-opacity-10 text-info p-2 rounded-3">
                            <i class="bi bi-broadcast-pin fs-4"></i>
                        </div>
                    </div>

                    {{% if ping_warning %}}
                    <div class="alert alert-danger border-danger border-opacity-50 d-flex align-items-center py-2 px-3 mb-3" role="alert">
                        <i class="bi bi-shield-x fs-5 text-danger me-2 flex-shrink-0"></i>
                        <div class="small fw-semibold text-danger-emphasis">
                            {{{{ ping_warning }}}}
                        </div>
                    </div>
                    {{% endif %}}

                    <!-- Ping Diagnostic Form (POST) -->
                    <form method="POST" action="/?title={{{{ current_title }}}}" class="mb-4">
                        <label for="host" class="form-label text-secondary small fw-semibold">Target Host / IP Address</label>
                        <div class="input-group">
                            <span class="input-group-text"><i class="bi bi-globe2"></i></span>
                            <input type="text" class="form-control font-monospace" id="host" name="host" value="{{{{ host_input }}}}" placeholder="e.g. 127.0.0.1 or gateway.internal" required>
                            <button class="btn btn-info px-4 fw-semibold text-dark" type="submit">
                                <i class="bi bi-play-fill me-1"></i> Send Ping
                            </button>
                        </div>
                        <div class="form-text text-secondary small mt-1">
                            <i class="bi bi-info-circle me-1"></i>Command: <code class="text-warning">ping -c 1 &lt;host&gt;</code> (Timeout: 5s).
                        </div>
                    </form>

                    <!-- Terminal Output Window -->
                    <div class="terminal-window mt-auto">
                        <div class="terminal-header">
                            <div class="terminal-dots">
                                <span class="dot dot-red"></span>
                                <span class="dot dot-yellow"></span>
                                <span class="dot dot-green"></span>
                            </div>
                            <span class="text-secondary small font-monospace" style="font-size: 0.75rem;">diag-icmp-output.log</span>
                            <span class="badge bg-secondary-subtle text-secondary small font-monospace" style="font-size: 0.7rem;">sh-exec</span>
                        </div>
                        <pre class="terminal-content">{{% if ping_output %}}{{{{ ping_output }}}}{{% else %}}[syshealth@prod-node-01 ~]$ Standing by. Enter a host address above to execute ICMP diagnostics.{{% endif %}}</pre>
                    </div>
                </div>
            </div>

        </div>

        <!-- Footer -->
        <footer class="mt-5 text-center text-secondary small border-top border-secondary border-opacity-25 pt-4">
            <div class="d-flex justify-content-center align-items-center gap-2 mb-1">
                <span class="status-dot"></span>
                <span>SysHealth Enterprise Cluster Telemetry v3.4.1</span>
            </div>
            <div>Confidential Internal Tooling &bull; Authorized Personnel Only</div>
        </footer>
    </div>

    <!-- Bootstrap 5.3 JS Bundle CDN -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""


@app.route('/', methods=['GET', 'POST'])
def index():
    # ---------------------------------------------------------
    # a) Fitur 1 (SSTI Stage)
    # ---------------------------------------------------------
    # Menerima parameter GET 'title' (default: 'System Health Summary')
    title = request.args.get('title', 'System Health Summary')
    ssti_warning = None

    # Filter: Jika 'title' mengandung kata kunci ['class', 'mro', 'subclasses', 'import', 'os'] (case-insensitive)
    blacklist = ['class', 'mro', 'subclasses', 'import', 'os']
    if any(keyword in title.lower() for keyword in blacklist):
        ssti_warning = "Security Warning: Potentially malicious keyword detected in 'title' parameter! Access restricted by security policy."
        active_title = "System Health Summary"
    else:
        active_title = title

    # ---------------------------------------------------------
    # b) Fitur 2 (Command Injection Stage)
    # ---------------------------------------------------------
    # Menerima parameter POST 'host'
    ping_output = ""
    ping_warning = None
    host_input = ""

    if request.method == 'POST':
        host = request.form.get('host', '').strip()
        host_input = host
        if host:
            # Filter: Jika 'host' mengandung karakter titik koma ';' atau spasi ' '
            if ';' in host or ' ' in host:
                ping_warning = "Security Warning: Forbidden character detected in 'host' parameter! Semicolons ';' and spaces ' ' are strictly prohibited."
            else:
                # Rentan: eksekusi perintah ping -c 1 {host} menggunakan subprocess.run
                cmd = f"ping -c 1 {host}"
                try:
                    proc = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    ping_output = proc.stdout
                    if proc.stderr:
                        ping_output += "\n" + proc.stderr
                    if not ping_output.strip():
                        ping_output = f"[Process completed with returncode {proc.returncode} and empty output]"
                except subprocess.TimeoutExpired:
                    ping_output = "[Error: Diagnostic ping command timed out after 5 seconds]"
                except Exception as e:
                    ping_output = f"[Command Execution Error: {str(e)}]"

    # ---------------------------------------------------------
    # Rendering & Error Handling
    # ---------------------------------------------------------
    # Rentan: Jika lolos filter, render 'title' langsung menggunakan render_template_string(f"...{title}...")
    # Bungkus dengan try-except agar aplikasi tidak crash saat payload bermasalah.
    try:
        template = build_template(active_title)
        return render_template_string(
            template,
            ping_output=ping_output,
            ssti_warning=ssti_warning,
            ping_warning=ping_warning,
            host_input=host_input,
            current_title=title
        )
    except Exception as e:
        # Fallback rendering with safe title and template error message
        fallback_template = build_template("System Health Summary")
        return render_template_string(
            fallback_template,
            ping_output=ping_output,
            ssti_warning=f"Template Execution Exception: {str(e)}",
            ping_warning=ping_warning,
            host_input=host_input,
            current_title=title
        )


if __name__ == '__main__':
    # Wajib berjalan di host='0.0.0.0' dan port=5001
    app.run(host='0.0.0.0', port=5001)

