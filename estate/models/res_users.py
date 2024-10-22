from odoo import fields, models


class resUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="seller_id", domain=[('state', 'in', ['new', 'offer received'])])
