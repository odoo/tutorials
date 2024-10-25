from odoo import api, fields, models
from odoo.fields import One2many


class EstatePropertyType(models.Model):
    _name = 'estate.property.types'
    _description = 'Model representing the different types of properties'
    _order = 'name'

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Property Ids")
    sequence = fields.Integer(string='Sequence')
    offer_ids = One2many('estate.property.offer', 'property_type_id', string="Offer Ids")
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)', "This property type already exists."),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
