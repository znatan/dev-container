FROM python:3.9

# Install development tools
RUN apt-get update && apt-get install -y \
    git \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Set up SSH server
RUN mkdir /run/sshd
RUN echo "root:password" | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Python packages for development
RUN pip install pylint autopep8 pytest

WORKDIR /workspace

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]