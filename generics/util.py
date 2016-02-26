#!/usr/local/bin/python

''' util.py
    -------
    @author = Ankai Lou
    -------------------
    Utility function & variables for generic class files
'''

###############################################################################
######################## import libraries & frameworks ########################
###############################################################################

import re
from hashlib import *

###############################################################################
############## global variables --- MODIFY HERE TO ALTER RESULTS ##############
###############################################################################

tag2meta = {'b'      : md5('b').hexdigest(),
            'dd'     : md5('dd').hexdigest(),
            'dl'     : md5('dl').hexdigest(),
            'dt'     : md5('dt').hexdigest(),
            'h1'     : md5('h1').hexdigest(),
            'h2'     : md5('h2').hexdigest(),
            'h3'     : md5('h3').hexdigest(),
            'h4'     : md5('h4').hexdigest(),
            'h5'     : md5('h5').hexdigest(),
            'h6'     : md5('h6').hexdigest(),
            'i'      : md5('i').hexdigest(),
            'li'     : md5('li').hexdigest(),
            'ol'     : md5('ol').hexdigest(),
            'strong' : md5('strong').hexdigest(),
            'sub'    : md5('sub').hexdigest(),
            'sup'    : md5('sup').hexdigest(),
            'table'  : md5('table').hexdigest(),
            'tbody'  : md5('tbody').hexdigest(),
            'td'     : md5('td').hexdigest(),
            'th'     : md5('th').hexdigest(),
            'tr'     : md5('tr').hexdigest(),
            'u'      : md5('u').hexdigest(),
            'ul'     : md5('ul').hexdigest(),}

###############################################################################
########################### function definition(s) ############################
###############################################################################

def deHTMLfy(content):
    ''' function: deHTMLfy
        ------------------
        encodes special formatting tags as meta-characters to be decoded
        ----------------------------------------------------------------
        @content    string to be encoded with meta-data tags
    '''
    content = re.sub(r'<!--.*-->','', content)
    for tag, meta in tag2meta.iteritems():
        content = re.sub(r'<%s.*>' % tag, '|%s|' % meta, content)
        content = re.sub(r'</%s.*>' % tag, '|/%s|' % meta, content)
    return content

