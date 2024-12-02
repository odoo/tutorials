from odoo import models, fields, api


class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is property Type table."
    _order = "sequence, name desc"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    number = fields.Integer(default=10)
    sequence = fields.Integer('Sequence', default=5)
    offer_count = fields.Integer(compute="_compute_offer_count")

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Property')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    
    _sql_constraints = [
        ('check_unique_type_name', 'UNIQUE(name)', 'This type is already exists.')
    ]
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
                record.offer_count = len(record.offer_ids)
