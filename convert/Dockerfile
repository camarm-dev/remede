# This Dockerfile is used to produce a single image to deploy a convert server, by copying ressources instead of creating volumes to the container
FROM amaccis/dict
COPY site.txt /etc/dictd_site.txt
COPY dictd.conf /etc/dictd.conf
COPY dictionaries/ /usr/lib/dict
EXPOSE 2628
