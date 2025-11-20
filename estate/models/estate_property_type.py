from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'All property types'
    _order = 'name asc'

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string="Properties",
    )
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_type_id', string="Offers",
    )
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
