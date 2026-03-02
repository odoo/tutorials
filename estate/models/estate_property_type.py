from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type module for Odoo 19 tutorials"
    _order = "sequence, name"

    name = fields.Char(required=True, string="Property Type Name")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties of this type")
    sequence = fields.Integer(default=1, string="Sequence")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers for this property type")
    offer_count = fields.Integer(compute="_compute_offer_count", string="Number of Offers")

    _check_unique_type_name = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.',
    )

    def _compute_offer_count(self):
        self.ensure_one()
        self.offer_count = len(self.offer_ids)
