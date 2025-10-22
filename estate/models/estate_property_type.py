from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "test description"
    _order = "sequence, name"

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages.")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer('Numbe of offers', compute='_compute_offers')

    @api.depends('offer_ids')
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _check_name = models.Constraint(
        'UNIQUE (name)',
        'The name must be unique',
    )
