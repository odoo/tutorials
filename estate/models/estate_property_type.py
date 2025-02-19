from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of estate"

    name = fields.Char('Name')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer('Offer Count', default=0, compute='_compute_offer_count')

    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'Name must be unique.'),
    ]

    _order = "sequence,name"

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
