# System Metrics Dashboard

A lightweight web application built with Flask to monitor system metrics in real-time. It tracks CPU, memory, and disk usage, streaming the data to a browser-based bar chart using Server-Sent Events (SSE) and Chart.js. The dashboard updates approximately every 1 second and displays the last 50 data points, providing a clear, large visualization of system performance.

## Features
- Real-time monitoring of:
  - CPU usage (%)
  - Memory usage (%)
  - Disk usage (%)
- Bar chart visualization powered by Chart.js.
- Automatic updates every ~1 second via Server-Sent Events (SSE).
- Large, responsive UI optimized for readability.
- No manual interaction required—fully automated display.

## Prerequisites
- **Python 3.x**: Verify with `python3 --version`.
- **Internet Connection**: Needed to load Chart.js from CDN.
- A system with accessible disk (e.g., `/` for Linux/macOS, `C:` for Windows).

## Setup Instructions
Follow these steps to set up and run the project locally.

### 1. Create the Project Directory
- Create a folder for the project:
  ```bash
  mkdir metrics_app
  cd metrics_app
  ```
- Ensure your `app.py` file is saved in this directory.

### 2. Set Up a Virtual Environment
- Create a virtual environment to isolate dependencies:
  ```bash
  python3 -m venv venv
  ```
- Activate it:
  - **Linux/macOS**:
    ```bash
    chmod +x ./venv/bin/activate
    . ./venv/bin/activate
    ```
  - **Windows**:
    ```bash
    venv\Scripts\activate
    ```
  - You’ll see `(venv)` in your terminal prompt when active.

### 3. Install Required Packages
- Install Flask and psutil within the virtual environment:
  ```bash
  pip install flask psutil
  ```

### 4. Run the Application
- Start the Flask server:
  ```bash
  python app.py
  ```
- Open a web browser and navigate to `http://localhost:5000`.

## Usage
- The dashboard loads at `http://localhost:5000` and displays a bar chart with:
  - **CPU Usage (%)**: Cyan bars.
  - **Memory Usage (%)**: Red bars.
  - **Disk Usage (%)**: Blue bars.
- Updates occur every ~1 second, showing the last 50 data points (~50 seconds of history).
- Metrics are automatically saved to `metrics.json` in the project folder.

## Project Structure
```
metrics_app/
├── app.py         # Flask application with SSE and Chart.js integration
├── venv/          # Virtual environment folder
└── metrics.json   # Generated file storing latest metrics
```

## Customization Options
- **Update Frequency**: Modify `interval=1` in `psutil.cpu_percent(interval=1)` to `0.5` for faster updates or `2` for slower.
- **Data Points**: Adjust `maxPoints = 50` in the JavaScript to `100` for more history or `20` for less.
- **Chart Type**: Change `type: 'bar'` to `'line'` or add `scales: { x: { stacked: true }, y: { stacked: true } }` for a stacked bar chart (see [Chart.js docs](https://www.chartjs.org/docs/latest/)).
- **UI Size**: Edit `max-width: 1200px` or `height: 600px` in the CSS for a different chart size.
- **Colors**: Update `backgroundColor` in the datasets (e.g., `'rgba(0, 255, 0, 0.7)'` for green bars).

## Troubleshooting
- **Chart Not Loading**:
  - Ensure internet access for the Chart.js CDN.
  - Check browser console (F12 → Console) for errors.
- **Updates Not Happening**:
  - Verify the `/metrics-stream` endpoint is streaming (F12 → Network tab).
  - Ensure `app.py` is running without errors.
- **Permission Issues**:
  - Check write permissions for `metrics_app` (`chmod -R u+w metrics_app` on Linux).
- **Port Conflict**:
  - If `5000` is in use, change `port=5000` to another (e.g., `port=5001`) in `app.run()`.

## Dependencies
- **Flask**: Web framework for serving the app and SSE.
- **psutil**: Python library for system metrics.
- **Chart.js**: JavaScript library for charting (loaded via CDN).

## Notes
- The update rate (~1 second) is tied to `psutil.cpu_percent(interval=1)`. Reducing `interval` below 0.5 may increase CPU load without improving accuracy.
- Disk usage is measured for the root partition (`/`). For Windows, replace `"/"` with `"C:"` in `psutil.disk_usage()` if needed.

## License
This project is open-source and unlicensed—use and modify it freely!

---

### How to Use This
1. In your `metrics_app` folder, create a file named `README.md`.
2. Copy the text above into it and save.
3. Open it in a Markdown viewer (e.g., VS Code, GitHub) to see it formatted.

This README assumes your latest code matches our recent iterations (bar chart, 50 points, ~1-second updates). If your code has unique features (e.g., different metrics, chart type), let me know, and I’ll tweak the documentation. How’s the project feeling for you now? Anything else you’d like in the README?