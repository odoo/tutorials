from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "sequence, name"

    name = fields.Char('Property Type', required=True)

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")

    offer_ids = fields.One2many('estate_property_offer', 'property_type_id', string='offers')

    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count', store=True)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    

    _sql_constraints = [
        ('check_type_uniqueness', 'UNIQUE(name)',
         'The new property type should be unique')
    ]
    