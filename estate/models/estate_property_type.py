from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'
    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'The name of the property type must be unique.'),
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        string="Properties",
        comodel_name='estate.property',
        inverse_name='property_type_id',
        help="Properties of this type.",
    )
    sequence = fields.Integer(
        default=1,
        help="Sequence of the property type for ordering.",
    )
    offer_ids = fields.One2many(
        string="Offers",
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
    )
    offer_count = fields.Integer(
        compute='_compute_offer_count',
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
