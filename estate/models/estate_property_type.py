from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count"
    )
    _unique_property_type = models.Constraint(
        'UNIQUE(name)',
        'The property type must be unique',
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
