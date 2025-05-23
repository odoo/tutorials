from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string='Offers',
    )
    sequence = fields.Integer("Sequence", default=1)
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Property type name must be unique."),
    ]

    @api.depends("property_ids.offer_ids")
    def _compute_offer_count(self):
        for prop_type in self:
            prop_type.offer_count = len(prop_type.mapped("property_ids.offer_ids"))
