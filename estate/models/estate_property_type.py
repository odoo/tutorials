from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "property types"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'type_id', string="property")
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="offer")
    offer_count = fields.Integer('Number of offers', compute="_compute_number_of_offers")

    _unique_name = models.Constraint(
        'unique(name)',
        'A property type must have a unique name.',
    )

    @api.depends('offer_ids')
    def _compute_number_of_offers(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
