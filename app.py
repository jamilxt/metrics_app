import psutil
import json
import time
from flask import Flask, Response, render_template_string

app = Flask(__name__)

# File to store metrics
JSON_FILE = "metrics.json"

# Function to collect system metrics
def collect_metrics():
    metrics = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent
    }
    return metrics

# SSE endpoint to stream metrics
@app.route("/metrics-stream")
def metrics_stream():
    def generate():
        while True:
            metrics = collect_metrics()
            yield f"event: metrics\ndata: {json.dumps(metrics)}\n\n"
    return Response(generate(), mimetype="text/event-stream")

# Frontend route with chart only (no button)
@app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>System Metrics Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 40px; 
                text-align: center; 
            }
            h1 { 
                font-size: 48px; 
            }
            canvas { 
                max-width: 1200px; 
                height: 600px !important; 
                margin: 40px auto; 
            }
        </style>
    </head>
    <body>
        <h1>System Metrics Dashboard</h1>
        <canvas id="metricsChart"></canvas>

        <script>
            // Set up Chart.js with larger fonts
            const ctx = document.getElementById('metricsChart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: 'CPU Usage (%)',
                            data: [],
                            borderColor: 'rgba(75, 192, 192, 1)',
                            fill: false
                        },
                        {
                            label: 'Memory Usage (%)',
                            data: [],
                            borderColor: 'rgba(255, 99, 132, 1)',
                            fill: false
                        },
                        {
                            label: 'Disk Usage (%)',
                            data: [],
                            borderColor: 'rgba(54, 162, 235, 1)',
                            fill: false
                        }
                    ]
                },
                options: {
                    scales: {
                        y: { 
                            beginAtZero: true, 
                            max: 100,
                            title: { display: true, text: 'Percentage (%)', font: { size: 20 } },
                            ticks: { font: { size: 16 } }
                        },
                        x: { 
                            title: { display: true, text: 'Time', font: { size: 20 } },
                            ticks: { font: { size: 16 } }
                        }
                    },
                    plugins: {
                        legend: { labels: { font: { size: 18 } } }
                    }
                }
            });

            // Function to update chart with new data
            function updateChart(metrics) {
                const maxPoints = 20;
                chart.data.labels.push(metrics.timestamp);
                chart.data.datasets[0].data.push(metrics.cpu_percent);
                chart.data.datasets[1].data.push(metrics.memory_percent);
                chart.data.datasets[2].data.push(metrics.disk_usage);

                if (chart.data.labels.length > maxPoints) {
                    chart.data.labels.shift();
                    chart.data.datasets.forEach(dataset => dataset.data.shift());
                }
                chart.update();
            }

            // Listen to SSE stream
            const source = new EventSource('/metrics-stream');
            source.addEventListener('metrics', function(event) {
                const data = JSON.parse(event.data);
                updateChart(data);
            });
            source.onerror = function() {
                console.log('SSE connection error. Reconnecting...');
            };
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)