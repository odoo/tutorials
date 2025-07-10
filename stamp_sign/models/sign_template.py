from odoo import fields, models


class SignItemType(models.Model):
    _inherit = "sign.item.type"

    item_type = fields.Selection(
        selection_add=[("stamp", "Stamp")], ondelete={"stamp": "set default"}
    )
