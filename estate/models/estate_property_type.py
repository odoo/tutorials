from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The types of real estate properties"
    _order = "sequence, name"
    _sql_constraints = [
        (
            'check_name',
            'UNIQUE(name)',
            'The name must be unique.',
        )
    ]

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_offers")

    @api.depends('offer_ids')
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
