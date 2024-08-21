from odoo import fields, models


class EstatePopertyUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson", string="Offers")
