##Установка и запуск на линукс (находясь в папке приложения):
docker build -t stable_diffusion_pyqt . 
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix stable_diffusion_pyqt
