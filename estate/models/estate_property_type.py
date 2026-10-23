from odoo import api, fields, models


class PropertyTypes(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"
    _order = "name"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(
        string="Number of Offers", compute="_compute_offer_count"
    )
    sequence = fields.Integer(string="Sequence", default=1)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _check_name = models.Constraint(
        "unique (name)",
        "A property type name must be unique.",
    )
