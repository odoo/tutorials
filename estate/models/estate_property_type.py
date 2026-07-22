from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "model for estate property types"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _unique_name = models.Constraint(
        "UNIQUE(name)", "Property type name must be unique."
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
