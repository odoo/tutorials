from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)

    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id')

    offer_count = fields.Integer(compute='_compute_offer_count', string="Offers")

    @api.depends('property_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.property_ids)
