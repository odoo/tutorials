from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The property Type'
    _order = 'sequence, name'
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    name = fields.Char(required=True)
    _sql_constraints = [
        ('type_name_unique', 'UNIQUE(name)', "The property type name must be unique.")
    ]
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Offers Count", compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
