from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Used to order property types manually"
    )

    name = fields.Char(required=True)

    # One2many vers le vrai modèle estate.property
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',  # le Many2one dans estate.property
        string="Properties"
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string="Offers"
    )

    offer_count = fields.Integer(
        string="Offer Count",
        compute='_compute_offer_count'
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _check_name_unique = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique.",
    )
