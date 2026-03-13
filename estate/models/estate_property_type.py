from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"
    _order = "name"

    name = fields.Char(string="Property Types", required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Property",
    )
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better.",
    )
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offers")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")

    _name_uniq = models.Constraint(
        "unique(name)",
        "A Property Type with the same name already exists.",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = self.env["estate.property.offer"].search_count(
                [("property_type_id", "=", record.ids)],
            )
