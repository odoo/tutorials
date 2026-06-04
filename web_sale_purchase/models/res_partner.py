from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_seller = fields.Boolean(default=False)
