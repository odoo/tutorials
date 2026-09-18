from odoo import models, fields


class ResUsers(models.Model):
    _inherit = ["res.users"]
    _name = 'res.users'

    property_ids = fields.One2many("estate.property", "salesperson_id", copy=False, domain="['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]")
