#!/bin/bash
set -e
exec > /var/log/user_data.log 2>&1

echo "============================================"
echo "Jenkins CI/CD Pipeline - Server Setup"
echo "Started: $(date)"
echo "============================================"

# System Update
echo "[1/6] Updating system packages..."
dnf update -y

# Install Java 17
echo "[2/6] Installing Java 17..."
dnf install -y java-17-amazon-corretto
java -version

# Install Jenkins
echo "[3/6] Installing Jenkins..."
wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
dnf install -y jenkins
systemctl enable jenkins
systemctl start jenkins

# Install Docker
echo "[4/6] Installing Docker..."
dnf install -y docker
systemctl enable docker
systemctl start docker
usermod -aG docker jenkins

# Install Python 3
echo "[5/6] Installing Python 3..."
dnf install -y python3 python3-pip

# Install Git
echo "[6/6] Installing Git..."
dnf install -y git

echo "============================================"
echo "Setup Complete: $(date)"
echo "Jenkins Status: $(systemctl is-active jenkins)"
echo "Docker Status:  $(systemctl is-active docker)"
echo "============================================"
