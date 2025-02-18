from odoo import api, fields, models


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
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
        string="Offers",
        help="List of offers related to properties of this type"
    )
    offer_count = fields.Integer(
        string="Offer Count",
        compute='_compute_offer_count',
        help="Total number of offers for properties of this type"
    )


    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for offer in self:
            offer.offer_count = len(offer.offer_ids)

    # SQL CONSTRAINTS
    _sql_constraints = [
        (
            'unique_type_name',
            'UNIQUE(name)',
            'Property Type name must be Unique.'
        )
    ]
