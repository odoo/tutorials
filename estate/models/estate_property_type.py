from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name'

    name = fields.Char(string="Property Type")
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
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
    sequence = fields.Integer(string="Sequence", default=1, help="Used to order property types. Lower is better.")

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'A property type must be unique.')
    ]

    def _compute_offer_count(self):
        for offer in self:
            offer.offer_count = len(offer.offer_ids)
