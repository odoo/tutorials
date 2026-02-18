from odoo import models, fields, api
from odoo.exceptions import ValidationError

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

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            existing = self.search([
                ('name', '=', record.name),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError("The property type name must be unique.")

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    expected_price = fields.Float()
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        default='new'
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type'
    )
