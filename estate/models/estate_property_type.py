from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of Real Estate Property"
    _order = "sequence desc"

    sequence = fields.Integer(
        "Sequence",
        default=1,
        help="Used to order stages. Lower is better.",
    )
    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Estate Properties",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Estate Properties Offers",
    )
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The name of a type should be unique.",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
