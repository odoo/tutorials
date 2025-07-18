from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of Estate property "
    _order = "sequence, name asc" 

    name = fields.Char(required=True)
    sequence = fields.Integer(
        "Sequence", default=10, help="Used to order property types."
    )

    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(
        string="Offer Count", compute="_compute_offer_count", store=True
    )

    _sql_constraints = [
        (
            "unique_property_type_name",
            "UNIQUE(name)",
            "A property type name must be unique.",
        ),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
