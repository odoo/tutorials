from odoo import models, fields


class Estate_property_type(models.Model):
    _name = "estate_property_type"
    _description = "APP super mega trop bien"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate_property_offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _check_name = models.Constraint(
        "UNIQUE(name)",
        message="The name of the property type must be unique",
    )
    property_ids = fields.One2many("estate_property", "property_type_id", string="Properties")

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
