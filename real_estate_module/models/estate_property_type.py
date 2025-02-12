from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Types such as Home, Apartment, etc."
    _order = 'name'

    name = fields.Char(
        string="Property Type",
        required=True,
        help="The name of the property type (e.g., Home, Apartment, Villa)"
    )

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string="Properties",
        help="List of properties belonging to this type"
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

    _sql_constraints = [
        (
            'unique_property_type_name',
            'UNIQUE(name)',
            "The name must be unique"
        )
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        """Compute the total number of offers for this property type."""
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
