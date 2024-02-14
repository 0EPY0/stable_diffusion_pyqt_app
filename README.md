# Docker install
docker build -t stable_diffusion_pyqt . 
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix stable_diffusion_pyqt

# Python install
pip install -r requirements.txt

# Внимание
Докер проверен на fedora 38, python3.11.
