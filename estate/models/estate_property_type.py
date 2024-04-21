from odoo import api, fields, models

class PropertyType(models.Model):

    _name = "estate_property_type"
    _description = "The type of the real estate property i.e. house, apartment, etc"
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name of the property type must be unique'),
    ]
    _order = 'name'
    property_ids = fields.One2many('estate_property', 'property_type_id')
    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help='Used for ordering property types. Lower is better')
    property_offer_ids = fields.One2many('estate_property_offer', 'property_type_id')
    property_offer_count = fields.Integer(compute="_compute_property_offer_count")

    @api.depends('property_offer_ids')
    def _compute_property_offer_count(self):
        for record in self:
            record.property_offer_count = len(record.property_offer_ids)
