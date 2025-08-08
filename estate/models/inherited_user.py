# Imports of odoo
from odoo import fields, models


class InheritedUser(models.Model):
    # === Private attributes ===
    _inherit = 'res.users'

    # === Fields declaration ===
    property_ids = fields.One2many('estate.property', 'salesman_id', string="Properties")
