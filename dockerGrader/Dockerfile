FROM base/archlinux
WORKDIR /tmp
RUN pacman -Syu wget --noconfirm
RUN wget https://repo.anaconda.com/archive/Anaconda3-5.3.0-Linux-x86_64.sh
RUN chmod +x *.sh
RUN ./Anaconda*.sh -b
ENV PATH="/root/anaconda3/bin:${PATH}"
