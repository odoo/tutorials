from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = 'sequence,name'

    name = fields.Char(required=True)
    sequence = fields.Integer('sequence')
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', "property_type_id")
    offer_count = fields.Integer(compute='_compute_offer_count')

    _unique_type = models.Constraint(
        'unique(name)',
        'Property type should be unique'
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
