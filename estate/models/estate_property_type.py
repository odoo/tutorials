from odoo import api, fields, models


class EstatePropertyTypeModel(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate property types database"
    _order = 'sequence, name'
    _name_check = models.Constraint('UNIQUE(name)', "The name must be unique.")

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
