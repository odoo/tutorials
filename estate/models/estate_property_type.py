from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Types for our properties'
    _order = "sequence, name"
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
        'The property type names MUST be unique.'),
    ]

    name = fields.Char(required=True)
    sequence = fields.Integer()

    # Relations
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id')

    # computed
    offer_count = fields.Integer(compute='_compute_offer_count')

    # region Compute methodes
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(self.offer_ids)

    # endregion
