from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char('Property Type Name', required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(
        compute="_compute_offer_count", string="Number of Offers")
    sequence = fields.Integer(default=1)

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Property type names must be unique.",
    )

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
