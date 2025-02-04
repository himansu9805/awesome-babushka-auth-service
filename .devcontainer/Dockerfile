FROM archlinux:latest

# Install packages
RUN pacman -Syu --noconfirm \
    base-devel \
    git \
    cmake \
    clang \
    lldb \
    python \
    python-pip \
    nodejs \
    npm \
    wget \
    unzip \
    iputils \
    gcc \
    curl \
    vim \
    tree \
    less

# Create pip config directory and add configuration
RUN mkdir -p /root/.config/pip && \
    echo -e "[global]\nbreak-system-packages = true\nroot-user-action = ignore" > /root/.config/pip/pip.conf

RUN git config --global core.editor "vim"
