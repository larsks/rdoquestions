#!/usr/bin/python

import os
import sys
import argparse
import yaml
import logging
import bottle
import functools
import jinja2

import askbot

from . import settings
from .templates import view

app = bottle.app()

with open(os.environ.get('RDOQUESTIONS_CONFIG_FILE', 'askbot.yaml')) as fd:
    cfg = yaml.load(fd)

@bottle.hook('before_request')
def setup_askbot_object():
    bottle.request.askbot = askbot.Askbot(
        endpoint=cfg['endpoint'])

@view('questions')
def unanswered(tags=None):
    limit = bottle.request.params.get('l', cfg.get('limit'))
    sortkey = bottle.request.params.get('s', 'age')
    sortorder = bottle.request.params.get('o', 'asc')

    q = bottle.request.askbot.questions(
        tags=tags, scope='unanswered',
        sort='%s-%s' % (sortkey, sortorder), limit=limit
    )

    return {'questions': q,
            'tags': tags,
            'baseurl': cfg['baseurl'],
            }

@app.route('/unanswered/tag/<tag>')
def unanswered_tag(tag):
    return unanswered(tags=[tag])

@app.route('/unanswered')
def unanswered_all():
    return unanswered()

@app.route('/assets/<path:path>')
def asset(path):
    return bottle.static_file(path, root=settings.assets_dir)

@app.route('/')
def index():
    bottle.redirect('/unanswered')

