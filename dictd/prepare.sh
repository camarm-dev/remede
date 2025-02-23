#! /bin/bash

python3 dictd/prepare.py
cd dictd/dictionnaries
dictfmt -e --utf8 --allchars -s "Remède Français" remede < remede.txt
dictfmt -e --utf8 --allchars -s "Remède English" remede.en < remede.en.txt
# TODO zip dicts
