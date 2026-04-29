from odoo import fields, models


class Estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "APP super mega trop bien"
    _order = "sequence, name"
    _check_name = models.Constraint(
        "UNIQUE(name)",
        message="The name of the property type must be unique",
    )

    name = fields.Char(required=True)
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
