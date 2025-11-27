from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = "sequence, name"

    name = fields.Char('Property Type', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', 'Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', 'Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')
    sequence = fields.Integer()

    _type_name_uniq = models.Constraint(
        'unique(name)',
        "The property type name must be unique",
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
