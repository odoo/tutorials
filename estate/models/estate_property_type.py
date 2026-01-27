from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type."
    _order = "sequence, name"

    name = fields.Char('Property Type', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")
    offer_count = fields.Integer('Offer Count', compute='_compute_offer_count')
    property_ids = fields.One2many('estate.property', 'type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')

    ## CONSTRAINTS ##
    _check_name = models.Constraint(
        'UNIQUE(name)',
        'The type must be unique.',
    )

    ## COMPUTED ##
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
