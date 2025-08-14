from odoo import api, models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer('Sequence', default=10)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offers Count", compute='_compute_offer_count')

    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)', 'The property type name must be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for prop_type in self:
            prop_type.offer_count = len(prop_type.offer_ids)
