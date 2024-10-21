from odoo import api, models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Type of a property'
    _order = 'sequence asc, name asc'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer(string='Sequence', default=10, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Offer count', compute='_compute_offer_count')

    _sql_constraints = [
        ('Unique_name', 'unique (name)',
         'This type name already exists'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
