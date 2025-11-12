from odoo import models,fields

class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    property_ids = fields.One2many("estate.property", "user_id", string="Properties", domain="[('state', 'not in', ['sold', 'cancelled'])]")
