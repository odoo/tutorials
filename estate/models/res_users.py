from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'salesperson_id',
     domain="['|',('status', '=', 'new'),('status', '=', 'offer_received')]")
