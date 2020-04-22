#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
    Module dedicated to computational functions
    These functions does not need network
    to properly return something
"""

from __future__ import print_function
import subprocess
from passlib import pwd
from passlib.hash import sha256_crypt
from passlib.hash import sha512_crypt


def _compute_clear_passwordlist(count):
    """internal unique routine to compute passwords"""
    return pwd.genword(
        length=16,
        entropy=56,
        chars="aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789&~\#{[|^@]}$%*,?.;/:!=+)(-'",
        returns=count,
    )


def compute_uhash(count):
    """Generate linux system user couple of clear/hashes passwords (SHA512)"""
    result = dict()
    for i in _compute_clear_passwordlist(count):
        hashed = sha512_crypt.hash(i)
        if sha512_crypt.verify(i, hashed):
            result[sha512_crypt.hash(i)] = i
    return compute_markdown_rendering(1, result)


def compute_mhash(count):
    """Generate mysql 5.6+ system user couple of clear/hashes passwords """
    result = dict()
    for i in _compute_clear_passwordlist(count):
        hashed = sha256_crypt.hash(i)
        if sha256_crypt.verify(i, hashed):
            result[sha256_crypt.hash(i)] = i
    return compute_markdown_rendering(1, result)


def compute_cpwd(count):
    """Generate clear password."""
    return compute_markdown_rendering(2, _compute_clear_passwordlist(count))


def compute_markdown_rendering(rendertype, text):
    """Generate special markdown rendering."""
    rendered = ""
    if text:
        if rendertype == 1:
            for key, value in text.items():
                rendered += "* " + key + " ### " + value + "\n"
        elif rendertype == 2:
            for i in text:
                rendered += "* " + i + "\n"
        elif rendertype == 3:
            for key, value in text.items():
                rendered += "* " + key + ": " + str(value) + "\n"
        elif rendertype == 4:
            rendered = "[![](" + text + ")](" + text + ")"
        else:
            rendered = text
    else:
        text = "Something weird happened :("
    return rendered


def compute_kamoulox(query):
    """get french Kamoulox !"""
    param = "-n" + "1"
    result = []
    if query in ("kamounom", "kamouscuse", "kamousulte", "kamoumail"):
        process = subprocess.run(
            ["kamoulox", query, param],
            stdout=subprocess.PIPE,
            check=True,
            universal_newlines=True,
        )
        for line in process.stdout.splitlines():
            result.append(str(line))
    else:
        process = subprocess.run(
            ["kamoulox", param],
            stdout=subprocess.PIPE,
            check=True,
            universal_newlines=True,
        )
        for line in process.stdout.splitlines():
            result.append(str(line))
    return compute_markdown_rendering(2, result)
