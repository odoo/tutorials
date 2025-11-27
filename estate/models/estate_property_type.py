from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'
    _order = 'name'
    _name_unique = models.Constraint(
        'unique (name)',
        'A property type of that name already exists',
    )

    name = fields.Char('Property Type', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1)
    offer_count = fields.Integer('Number of offers', default=0, compute="_compute_offers_count")

    @api.depends("property_ids")
    def _compute_offers_count(self):
        for record in self:
            record.offer_count = sum(len(property.offer_ids) for property in record.property_ids)
