# Team-Aetherion Repository

Welcome to the Team-Aetherion repository for advanced computer vision and machine learning projects.

## 📁 Projects

### Prakhar - UOWD Aerospace Machine Vision System
Advanced computer vision system for real-time object detection, shape recognition, and color analysis.

**Features:**
- Real-time object detection with live camera feed
- Shape recognition (10+ shapes) & color detection with hex values
- Edge detection algorithms & object tracking
- Docker containerization support
- AWS deployment ready

**Quick Start:**
```bash
cd Prakhar/
python machine_vision.py    # Basic version
python advanced_machine_vision.py  # Advanced version
```

**Docker Deployment:**
```bash
cd Prakhar/
docker build -t team-aetherion-vision .
docker run --rm -it --device /dev/video0 team-aetherion-vision
```

## Team Members
- **Prakhar** - Machine Vision Systems & Computer Vision

## License
MIT License - See individual project folders for specific details.
