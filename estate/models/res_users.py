from odoo import api, fields, models

class InheritedResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property','user_id', domain="[('state', 'not in', ['sold', 'cancelled'])]")
