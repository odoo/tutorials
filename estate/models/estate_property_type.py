from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "estate property type description"

    # Ordering
    sequence = fields.Integer('Sequence', default=1, help="Used to order types.")
    name = fields.Char('Property Type', required=True)
    _order = "sequence, name"

    name = fields.Char('Property Type', required=True)
    description = fields.Char('Description', required=False)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    # Relations
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id', string='Offers')
    offer_count = fields.Integer('Offer Count', compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
