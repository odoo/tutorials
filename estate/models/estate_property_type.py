from odoo import api, models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    estate_property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique',
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids or [])
