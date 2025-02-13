from odoo import _, api, fields, models


class EsatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequemce', default=2)
    property_type_ids = fields.One2many('estate.property','property_type_id', store=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(string='Count', compute="_count_offer_ids")

    _sql_constraints = [
        ('type_unique','UNIQUE(name)','The name must be unique'),
    ]

    @api.depends('offer_ids')
    def _count_offer_ids(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
