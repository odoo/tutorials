from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson", domain="[('state', 'in', ('new', 'offer received'))]")
