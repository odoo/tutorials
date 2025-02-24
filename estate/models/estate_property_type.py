from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'estate property type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property','property_type_id')
    sequence = fields.Integer(default=1, help='helps in ordering of views in ui')
    offer_ids = fields.One2many(related='property_ids.offer_ids', inverse_name='property_type_id', store=True)
    offer_count = fields.Integer(compute='_compute_offers')
    
    _sql_constraints =[
        ('_unique_name','UNIQUE(name)','Property type must be unique'),
    ]

    @api.depends('offer_ids')
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
