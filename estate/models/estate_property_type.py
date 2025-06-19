from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real estate property Type"
    _order = 'sequence, name ASC'

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         "This property type already exists."),
    ]
