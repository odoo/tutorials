from odoo import fields, api, models


class EstatePropertiesType(models.Model):
    _name = 'estate.properties.type'
    _description = 'Estate Properties Type'
    _order = 'name'

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.properties', 'property_type_id', string='Properties')
    sequence = fields.Integer()
    offer_ids = fields.One2many(
        'estate.properties.offer', 'property_type_id', string='Offer')
    offer_count = fields.Integer(compute='_compute_offer_count', store=True)

    _sql_constraints = [
        ('name', 'UNIQUE(name)',
         'Property Type should be unique')
    ]

    def redirect_offer_form(self):
        return {
            'name': 'Offer',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.properties.offer',
            'views': [[False, 'list'], [False, 'form']],
            'target': 'current',
            'domain': [['property_type_id', '=', self.id]],
            'context': [['default_property_type_id', '=', self.id]],
        }

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
