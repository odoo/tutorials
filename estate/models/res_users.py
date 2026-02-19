from odoo import fields, models


class ResUsers(models.Model):
    _name = "res.users"
    _description = "Adding fields for the user model"
    _inherit = ['res.users']

    property_ids = fields.One2many(
        'estate.property',
        'salesman_id',
        string="Estates",
        domain="['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]",
        )
