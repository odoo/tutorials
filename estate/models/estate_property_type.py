from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    offer_count = fields.Integer(compute="_compute_offer_count")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    property_ids = fields.One2many('estate.property', 'property_type_id')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
