from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = "name"
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    name = fields.Char(string="Name", required=True, index=True)
    expected_price = fields.Float(string="Expected Price")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_type_id"
    )
    offer_count = fields.Integer(compute="_compute_offer_count")
    _sql_constraints = [
        ("name_uniq", "unique(name)", "Type must be unique"),
    ]

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

  