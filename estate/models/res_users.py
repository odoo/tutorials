from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name="estate.property", 
        inverse_name="salesperson_id", 
        domain=[("state", "in", ["new", "offer received"])])
