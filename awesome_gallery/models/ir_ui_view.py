from odoo import fields, models


class View(models.Model):
    _inherit = "ir.ui.view"

    type = fields.Selection(selection_add=[("gallery", "Awesome Gallery")])

    def _get_view_info(self):
        old = super()._get_view_info()
        old["gallery"] = {"icon": "fa fa-image"}
        return old
