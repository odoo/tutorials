from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Type of a property'
    _order = "sequence, name asc"
    _sql_constraints = [
        ('check_unicity', 'UNIQUE (name)', 'A property type with the same name already exists'),
    ]

    name = fields.Char('Property Type', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer('Offer Count', compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
