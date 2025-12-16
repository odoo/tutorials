from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type')
    offer_ids = fields.One2many(comodel_name="estate.property.offers", inverse_name="property_type_id", string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
