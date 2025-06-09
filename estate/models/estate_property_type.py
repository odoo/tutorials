from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = 'name'

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string='Properties'
    )
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_type_id', string='Offers'
    )
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer Count')

    _sql_constraints = [
        ('check_property_type', 'UNIQUE(name)', 'Property Type must be unique'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
