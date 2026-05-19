from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type Model"
    _order = 'name'

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string="Properties"
    )
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_type_id', string="Offers"
    )
    offer_count = fields.Integer(compute='_compute_offer_count')

    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'Type name must be unique.'
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids or [])
