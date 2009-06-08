#!/usr/bin/python
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from markdown import markdown

from django.contrib.markup.templatetags.markup import restructuredtext
from django.utils.html import strip_tags, urlize
from django_utils import clean_html, clean_tiny_mce_prefix

from bbcode import markup as bbcode_markup

class Markup(object):
    safe = False
    allow_urlize = True

    def urlize(self, data):
        """
        Urlize plain text links in the HTML contents.
       
        Do not urlize content of A and CODE tags.
        """
    
        soup = BeautifulSoup(data)
        for chunk in soup.findAll(text=True):
            islink = False
            ptr = chunk.parent
            while ptr.parent:
                if ptr.name == 'a' or ptr.name == 'code':
                    islink = True
                    break
                ptr = ptr.parent
    
            if not islink:
                chunk = chunk.replaceWith(urlize(unicode(chunk), trim_url_limit=40))
        return unicode(soup)
    
    def render(self, value, urlize=True, fix_tinymce=True, **kwargs):
        value = self.do_render(value)
        if urlize and self.allow_urlize:
            value = self.urlize(value)
        if fix_tinymce:
            value = clean_tiny_mce_prefix(value)    # TinyMCE bug
        return value
        
    def do_render(self, value, **kwargs):
        return value

class Markdown(object):
    safe = True

    def do_render(self, value, urlize=True, **kwargs):
        return markdown(value)

class RawHTML(Markup):
    pass

class SafeHTML(Markup):
    safe = True
    
    def do_render(self, value, **kwargs):
        return clean_html(value)

class PlainText(Markup):
    safe = True
    allow_urlize = False

    def do_render(self, value, **kwargs):
        return strip_tags(value)

class BBCode(Markup):
    safe = True

    def do_render(self, value, **kwargs):
        return bbcode_markup(value, auto_urls=False)

class Restructured(Markup):
    safe = True
    
    def do_render(self, value, **kwargs):
        value = restructuredtext(value)

# =\
class Library(object):
    MARKUPS = {
        'markdown': Markdown(),
        'raw html': RawHTML(),
        'safe html': SafeHTML(),
        'plain text': PlainText(),
        'bbcode': BBCode(),
        'rest': Restructured(),
    }
    clean = True
    
    @classmethod
    def dirty(cls):
        cls.clean = False
        
    @classmethod
    def register(cls, name, markup_cls):
        # All markups should be registered before usage
        # TODO: new Error classes
        if isinstance(markup_cl):
            raise Exception(u'Not Allowed class')
        if not cls.clean:
            raise Exception(u'Registering classes after first usage')
        cls[name] = markup_cls

