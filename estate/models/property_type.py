from odoo import api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Type"
    _order = "sequence desc, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(help="Used to order property types. Higher is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _name_uniq = models.Constraint("UNIQUE(name)", "The name must be unique.")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
