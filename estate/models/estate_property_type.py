from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    name = fields.Char(required=True)
    property_id = fields.One2many('estate.property', 'property_type_id')
    _order = 'sequence, name'
    sequence = fields.Integer('Sequence', help="Used to order stages. Lower is better.")
    offers_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_offers_count', help="Number of offers")

    @api.depends('offers_ids.property_type_id')
    def _offers_count(self):
        for record in self:
            if record.offers_ids:
                record.offer_count = len(record.offers_ids)
            else:
                record.offer_count = 0
