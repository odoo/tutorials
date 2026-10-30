from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name'

    name = fields.Char('Property Types', required=True)
    sequence = fields.Integer('Sequence', default=1, help='Used to order property types.')
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_count = fields.Integer('Offers', compute='_compute_offer_count')
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")

    _name_must_be_unique = models.Constraint(
        "UNIQUE(name)",
        "Property type name must be unique",
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        self.offer_count = len(self.offer_ids)
