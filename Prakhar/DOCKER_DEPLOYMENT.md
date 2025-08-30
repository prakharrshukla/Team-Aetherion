# Team-Aetherion Machine Vision - Docker Deployment Guide

## Overview
This guide helps you deploy the UOWD Aerospace Machine Vision System using Docker containers.

## Prerequisites
- Docker installed on your system
- Camera/webcam access (for local deployment)
- Git (to clone the repository)

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/prakharrshukla/Team-Aetherion.git
cd Team-Aetherion/Prakhar
```

### 2. Build Docker Image
```bash
docker build -t team-aetherion-vision .
```

### 3. Run Container (Local with Camera)
```bash
# Linux/Mac - with camera access
docker run --rm -it --device /dev/video0 team-aetherion-vision

# Windows - with Docker Desktop
docker run --rm -it team-aetherion-vision
```

## Advanced Deployment Options

### AWS EC2 Deployment
```bash
# 1. Launch EC2 instance with Docker
# 2. Clone repository
git clone https://github.com/prakharrshukla/Team-Aetherion.git
cd Team-Aetherion/Prakhar

# 3. Build and run
docker build -t team-aetherion-vision .
docker run --rm -d --name vision-system team-aetherion-vision
```

### Docker Hub Deployment
```bash
# Tag and push to Docker Hub
docker tag team-aetherion-vision prakharrshukla/team-aetherion-vision:latest
docker push prakharrshukla/team-aetherion-vision:latest

# Pull and run from anywhere
docker pull prakharrshukla/team-aetherion-vision:latest
docker run --rm -it prakharrshukla/team-aetherion-vision:latest
```

### Environment Variables
```bash
# Custom configuration
docker run --rm -it \
  -e CAMERA_INDEX=0 \
  -e DETECTION_THRESHOLD=0.5 \
  team-aetherion-vision
```

## Container Specifications

**Base Image:** Python 3.11-slim  
**Dependencies:** OpenCV 4.12.0+, NumPy 2.2.6+, Pillow 10.0.1+  
**Default Port:** 8501 (for future web interface)  
**Entry Point:** `machine_vision.py`

## Customization

### Change Default Application
Edit the `CMD` line in `Dockerfile`:
```dockerfile
# Run advanced version
CMD ["python", "advanced_machine_vision.py"]

# Run demo mode
CMD ["python", "demo.py"]

# Run tests
CMD ["python", "test_system.py"]
```

### Add Web Interface Support
Add to `Dockerfile` before `CMD`:
```dockerfile
RUN pip install streamlit
EXPOSE 8501
CMD ["streamlit", "run", "web_interface.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Troubleshooting

### Camera Access Issues
- **Linux:** Ensure user is in `video` group
- **Windows:** Use Docker Desktop with camera sharing enabled
- **AWS:** Use IP camera or video stream instead of local camera

### Memory Issues
```bash
# Increase memory limit
docker run --rm -it -m 2g team-aetherion-vision
```

### Display Issues (Headless)
```bash
# Run without GUI (for server deployment)
docker run --rm -it -e DISPLAY=:99 team-aetherion-vision
```

## Production Deployment

### Docker Compose (Multi-Container)
```yaml
version: '3.8'
services:
  vision-system:
    build: .
    image: team-aetherion-vision
    ports:
      - "8501:8501"
    devices:
      - "/dev/video0:/dev/video0"
    restart: unless-stopped
```

### Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
  CMD python -c "import cv2; print('OK')" || exit 1
```

## AWS Specific Deployment

### ECS Deployment
1. Push image to ECR
2. Create ECS task definition
3. Deploy to ECS cluster
4. Configure load balancer (if needed)

### Lambda Deployment (Serverless)
- Use smaller base image (python:3.11-alpine)
- Reduce dependencies for faster cold starts
- Implement event-driven processing

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/prakharrshukla/Team-Aetherion/issues
- Repository: https://github.com/prakharrshukla/Team-Aetherion

**Team-Aetherion** - Advanced Technology Solutions
