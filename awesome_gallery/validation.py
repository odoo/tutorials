import logging
import os

from lxml import etree

from odoo.loglevels import ustr
from odoo.tools import misc, view_validation

_logger = logging.getLogger(__name__)


@view_validation.validate('gallery')
def schema_viewname(arch, **kwargs):
    if not hasattr(schema_viewname, "_gallery_validator"):
        with misc.file_open(os.path.join('awesome_gallery', 'rng', 'gallery_view.rng')) as f:
            schema_viewname._gallery_validator = etree.RelaxNG(etree.parse(f))

    validator = schema_viewname._gallery_validator

    if validator.validate(arch):
        return True

    for error in validator.error_log:
        _logger.error(ustr(error))
    return False
