from odoo import fields, models


class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = ["res.users"]

    property_ids = fields.One2many("estate.property", "salesman_id", string="Properties (estate)", domain=[("state", "in", ["new", "offer received"])])
