from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "estate property types"
    _order = 'name'

    # simple fields
    name = fields.Char('Type Name', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types.")

    # relational fields
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')

    # computed fields
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
