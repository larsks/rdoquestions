from __future__ import absolute_import

import os
import sys
import functools
import time

import jinja2
import markdown
from jinja2.loaders import FileSystemLoader

from . import settings

def filter_markdown (text):
    return markdown.markdown(text,
            extensions=[
                'fenced_code',
                'headerid',
                'attr_list',
                ])

def filter_strftime (text, format='%Y-%m-%d'):
    return time.strftime(format,
                         time.gmtime(int(text)))

template_env = jinja2.Environment(
        loader = FileSystemLoader(settings.template_dir))
template_env.filters['markdown'] = filter_markdown
template_env.filters['strftime'] = filter_strftime

template_globals = {
        'settings': settings,
        'environ': os.environ,
        }

def view(viewname):
    def view_decorator(f):
        @functools.wraps(f)
        def view_wrapper(*args, **kwargs):
            d = f(*args, **kwargs)

            if not isinstance(d, dict):
                return d

            for name in [viewname, '%s.html' % viewname]:
                try:
                    t = template_env.get_template(name,
                            globals=template_globals)
                    break
                except jinja2.TemplateNotFound:
                    pass
            else:
                raise KeyError(viewname)

            return t.render(**d)
        return view_wrapper

    return view_decorator

