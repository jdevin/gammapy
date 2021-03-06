# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from flask import Flask, Blueprint, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from .forms import CatalogBrowserForm

__all__ = ['catalog_browser']

log = logging.getLogger(__name__)

catalog_browser = Blueprint('catalog_browser', __name__, static_folder='static')


@catalog_browser.route('/', methods=['GET', 'POST'])
def view_index():
    form = CatalogBrowserForm()

    if form.validate_on_submit():
        session['catalog_name'] = form.catalog_name.data
        cat = source_catalogs[form.catalog_name.data]
        source = cat[form.source_name.data]
        session['source_name'] = form.source_name.data
        session['source_id'] = source.index
        session['info_display'] = form.info_display.data
        redirect(url_for('catalog_browser.view_index'))
    else:
        log.warning('Received invalid form. This should never happen!')

    return render_template('index.html',
                           form=form,
                           session=session,
                           )


@catalog_browser.route('/test')
def view_test():
    """A test page to try stuff out.
    """
    name = 'Johnny'
    return render_template('test.html', name=name)


def create_catalog_browser(config):
    try:
        import matplotlib
        matplotlib.use('agg')
    except ImportError:
        log.warning('Matplotlib not available.')

    app = Flask(__name__)
    app.register_blueprint(catalog_browser)
    app.secret_key = 'development key'
    Bootstrap(app)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    return app


from .api import *
