from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char("Property Type", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer("Sequence", default=1, help="Used to order property types")
    offer_ids = fields.One2many(related='property_ids.offer_ids', string="Offers", readonly=True)
    offer_count = fields.Integer("Offer Count", compute='_compute_offer_count')

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique"
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
