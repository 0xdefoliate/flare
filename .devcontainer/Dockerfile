# We use a minimal image to reduce attack surface
#
# We could've used Alpine Linux instead, but it was a bit of a
# headache, and this minimal Debian image is a good compromise.
FROM python:slim-trixie

# This is the bare minimum.
# Perhaps something is missing.
RUN apt update  -y && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
        ca-certificates \
        git             \
        ssh             \
        nano         && \
    apt autoremove   && \
    apt clean

RUN useradd -ms /bin/sh developer

# Principle of least privilege
USER developer