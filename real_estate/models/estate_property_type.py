from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = 'estate.property.type'
    _description = "Detail About Particular Property"
    _order = 'name asc'

    name = fields.Char(
        string="Name",
        required=True
    )
    sequence = fields.Integer(
        string="Sequence",
        default=3
    )

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string="Properties"
    )
    offer_ids=fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
        string="Offer"
    )
    offer_count=fields.Integer(
        string="Offer Count",
        compute='_compute_offer_count'
    )

    # SQL CONSTRAINTS
    _sql_constraints = [
        (
            'unique_type_name',
            'UNIQUE(name)',
            'Property Type name must be Unique.'
        )
    ]

    def _compute_offer_count(self):
        for offer in self:
            offer.offer_count = len(offer.offer_ids)
