from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Property type name must be unique')
    ]
    _order = 'sequence'
    
    sequence = fields.Integer('Sequence', default=10, help="Used to order property types. Lower is better.", required=True)
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offers Count", compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)