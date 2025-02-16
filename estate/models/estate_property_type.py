from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"
    _order = "name"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Price")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for count in self:
            result = self.env["estate.property.offer"]._read_group(
                domain=[("property_id.property_type_id", "=", count.id)],
                groupby=[],
                aggregates=["id:count"],
            )
            count.offer_count = result[0][0] if result else 0
