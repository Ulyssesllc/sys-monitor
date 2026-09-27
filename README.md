# 🚀 System Monitor CLI (`sys-monitor`)

[![CI](https://github.com/Ulyssesllc/sys-monitor/actions/workflows/ci.yml/badge.svg)](https://github.com/Ulyssesllc/sys-monitor/actions)
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![Coverage](https://img.shields.io/badge/coverage-%3E90%25-brightgreen.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
![Mypy](https://img.shields.io/badge/mypy-strict-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**sys-monitor** is a production-grade, high-performance Command-Line Interface (CLI) tool designed for real-time system resource monitoring (CPU, RAM, Disk), status alerting, and resource utilization trend visualization.

Built adhering to modern software engineering best practices, it features **Pandas Vectorization**, **Mypy Strict Type Checking**, **Pytest (Code Coverage >90%)**, **Docker Containerization**, and automated **GitHub Actions CI/CD**.

---

## ✨ Features & Highlights

- **⚡ Real-Time Resource Metrics**: Captures CPU, RAM, and Disk utilization using `psutil`.
- **🚀 High-Performance Vectorized Analysis**: Leverages **Pandas Vectorization** (`numpy.select`) to instantly classify status alerts (`OK`, `WARNING`, `CRITICAL`).
- **💻 Flexible CLI Interface**: Configurable via `argparse` options (`--interval`, `--count`, `--output-dir`, `--verbose`).
- **📊 Publication-Quality Trend Visualization**: Generates resource utilization charts with warning/critical threshold markers using **Matplotlib**.
- **📁 Multi-Format Report Export**: Automatically exports structured summary reports to **CSV** (`sys_summary.csv`) and **JSON** (`sys_summary.json`).
- **🛡️ Strict Code Quality**: Enforced with **Ruff** (Linter & Formatter) and **Mypy** (Strict Type Enforcement).
- **🐳 Docker Containerization**: Lightweight container execution powered by `python:3.12-slim`.
- **🔄 Automated CI/CD Pipeline**: GitHub Actions workflow automatically runs linter, static type checker, pytest suite, and verifies Docker builds on every push or Pull Request.

---

## 📂 Project Structure

```text
sys-monitor/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD Pipeline
├── reports/                # Output directory for CSV, JSON & PNG charts
│   ├── sys_summary.csv
│   ├── sys_summary.json
│   └── sys_metrics.png
├── collector.py            # Resource metrics collection & Pandas vectorization
├── visualize.py            # Matplotlib trend chart generation
├── main.py                 # Main CLI entrypoint and orchestration
├── test_monitor.py         # Pytest suite with code coverage
├── Dockerfile              # Docker containerization specification
├── pyproject.toml          # Python package definition & tool configuration
└── README.md               # Project documentation
```

---

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.12+**
- **Git**
- **Docker** (Optional for container deployment)

### Local Environment Setup

```bash
# Clone the repository
git clone https://github.com/Ulyssesllc/sys-monitor.git
cd sys-monitor

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in editable mode
pip install -e .
```

---

## 🚀 Usage

### 1. Execute via CLI (`sys-monitor`)

Once installed, invoke the `sys-monitor` command directly from your terminal:

```bash
# Run with default settings (5 samples at 1.0s interval)
sys-monitor

# Run with custom parameters
sys-monitor --count 10 --interval 2.0 --output-dir my_reports --verbose

# View CLI options and help documentation
sys-monitor --help
```

### 2. Execute via Docker

```bash
# Build the Docker image
docker build -t sys-monitor:latest .

# Run container and mount reports directory
docker run --rm sys-monitor:latest
```

---

## 🧪 Testing & Quality Assurance

### 1. Run Pytest with Code Coverage

```bash
pytest --cov=. --cov-report=term-missing
```

### 2. Code Quality & Type Checking

```bash
# Run Ruff Linter and Formatter check
ruff check .
ruff format --check .

# Run Mypy Static Type Analysis
mypy .
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

The repository includes a pre-configured GitHub Actions workflow in `.github/workflows/ci.yml`. On every `push` or `pull_request` targeting the `main` branch, the pipeline executes two sequential jobs:

1. **`test-and-lint`**: Installs dependencies, runs `ruff`, `mypy`, and executes `pytest` with a minimum coverage gate of **90%**.
2. **`docker-build`**: Verifies that the Docker container image builds cleanly without errors.

---

## 📄 License

This project is open-source and distributed under the **MIT License**.
