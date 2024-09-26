import logging

from odoo import registry

_logger = logging.getLogger(__name__)


def init_postgis_extension(env):
    # get a new cursor to avoid messing with the current transaction

    cr = registry(env.cr.dbname).cursor()
    cr.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    cr.commit()
