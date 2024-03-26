# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"
    sequence = fields.Integer('Sequence', default=1, help="used to order property types")

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Property Types")
    offers_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Nb. Offers", compute="_compute_offer_count")

    _sql_constraints = [
            ('name_unique', 'unique (name)', "Type name already exists!"),
        ]

    @api.depends('offers_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offers_ids)
