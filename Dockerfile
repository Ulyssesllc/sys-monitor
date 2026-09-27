FROM python:3.12-slim 

WORKDIR /app 

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/* 

COPY pyproject.toml README.md main.py collector.py visualize.py ./ 

RUN pip install --no-cache-dir . 

ENTRYPOINT ["sys-monitor"] 
CMD ["--count", "5", "--interval", "1.0", "--output-dir", "reports"]