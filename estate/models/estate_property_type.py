# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of existing properties"
    _order = "name"

    name = fields.Char('Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]

    @api.depends("offer_ids")
    def _compute_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
