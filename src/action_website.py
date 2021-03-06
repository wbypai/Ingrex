#coding=utf-8

from __future__ import unicode_literals
from packages.bottle import route, run
from ingrex import intel, praser


@route('/p/<pid>')
def portal(pid):
    return praser.portal(intel.fetch_portal(pid))


run(port=8080)
