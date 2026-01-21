from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )
    sequence = fields.Integer(string="Sequence", default=1)
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count",
    )

    _unique_name = models.Constraint(
        "UNIQUE (name)",
        "Name must be unique",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
