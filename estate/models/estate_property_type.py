from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Type"
    _order = 'sequence, name'

    name = fields.Char(required=True)
    offer_count = fields.Integer(
        compute='_compute_offer_count',
    )
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id'
    )
    sequence = fields.Integer()

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        "Property type name must be unique",
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        self.offer_count = len(self.offer_ids)
