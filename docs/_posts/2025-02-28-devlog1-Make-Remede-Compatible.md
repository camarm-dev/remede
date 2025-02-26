---
layout: post
title: "Remède Devlog 1 : Compatibility"
date: 2025-02-24
readable_date: 28 Février 2025
author: Armand
cover: /assets/devlog1.png
tags: 
  - Devlog
---

Hi everyone, in this article I will explain how and why the past weeks were dedicated to make Remède compatible
with old, but still used dictionaries formats, and some new functionalities I added.

## The DICT protocol

The DICT protocol was created by the DICT Development Group to provide a dictionary protocol over TCP/IP.
It has been described in the [RFC2229](https://www.rfc-editor.org/rfc/rfc2229) in October 1997.

Today it is still used by many dictionaries applications like the [Gnome dictionary](https://wiki.gnome.org/Apps/Dictionary),
Apple's macOS [Dictionary](https://en.wikipedia.org/wiki/Dictionary_(software)) or dictc for Windows.


So I decided to make Remède compatible with this protocol so everyone can use Remède databases with its own DICT client...

## Making Remède compatible with DICT

The easiest way to provide a DICT server is to use the `dictd` software. 
It is developed by DICT Development Group.

We just need to provide it our dictionaries in a special format. For that, I created a `prepare.py` script which transform
the Remède databases in a `.txt` compatible format. Then, it is easy to transform this `.txt` in `.dict` and `.index` files,
(which can be provided to `dictd`) using `dictfmt` utility (also developed by the DICT Development Group).

The dictd server is deployed at [dict.remede.camarm.fr](). I registered it on the [freedict DICT protocol server list](https://servers.freedict.org/).

I also added a support for the `dict://` url scheme, so Remède is interpreted as a dictionary application.

## The XML Dictionary eXchange Format

[XDXF](https://en.wikipedia.org/wiki/XDXF) (XML Dictionary eXchange Format) dictionary format created in 2006 whose goal is to unite all existing open dictionaries format.

Because it is widely compatible, to use or to convert dictionaries format, I decided to provide Remède dictionaries in XDXF.

To do so, I just use []() to convert from DICT format to XDXF.


All the dictionaries format mentioned above are now available in the Remède [release section](https://github.com/camarm-dev/remede) on Github. 


## Other improvements

I also worked on some new improvements for Remède.

- Performances were enhanced by a variable optimisation
- A "news" section has been added to the home page
- The blog has been enhanced

Thank you for reading this short devlog... I will often write dev article about Remède now.

See you later,

Armand, the Remède maintainer.
