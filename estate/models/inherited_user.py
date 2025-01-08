
from odoo import fields, models


class Inherited_User(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('test.property', 'sales_person_id', string='property')