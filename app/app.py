from flask import Flask, jsonify
import datetime
import os
import socket
import platform
import psutil

app = Flask(__name__)

def get_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024

@app.route("/")
def home():
    return jsonify({
        "app": "Jenkins CI/CD Pipeline — System Info Dashboard",
        "author": "Venkaiah Malli",
        "github": "github.com/venkaiahmalli96/jenkins-cicd-pipeline",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200

@app.route("/sysinfo")
def sysinfo():
    return jsonify({
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "cpu_cores": psutil.cpu_count(),
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "memory_total": get_size(psutil.virtual_memory().total),
        "memory_used": get_size(psutil.virtual_memory().used),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_total": get_size(psutil.disk_usage('/').total),
        "disk_used": get_size(psutil.disk_usage('/').used),
        "disk_percent": psutil.disk_usage('/').percent,
        "uptime_seconds": int(datetime.datetime.now().timestamp() - psutil.boot_time()),
        "app_version": os.getenv("APP_VERSION", "1.0.0"),
        "deployed_at": datetime.datetime.utcnow().isoformat() + "Z"
    })

@app.route("/version")
def version():
    return jsonify({
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "deployed_at": datetime.datetime.utcnow().isoformat() + "Z"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
