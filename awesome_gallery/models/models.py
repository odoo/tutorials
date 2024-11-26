from odoo import api, models
from lxml.builder import E


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _get_default_gallery_view(self):
        return E.gallery(string=self._description)
