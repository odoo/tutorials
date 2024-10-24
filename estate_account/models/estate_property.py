from odoo import fields, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    property_ids = fields.One2many(
        "estate.property", inverse_name="salesman_id", string="Properties"
    )
