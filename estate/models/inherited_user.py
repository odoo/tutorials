from odoo import fields, models

class InheritedUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'salesperson_id', string="Related Properties", domain="['|', ('state', '=', 'new'), ('state', '=', 'offerreceived')]")