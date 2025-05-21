from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=10)

    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )

    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer")
    offer_ids = fields.Many2many(
        "estate.property.offer", string="Offers", compute="_compute_offer"
    )

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    def _compute_offer(self):

        data = self.env["estate.property.offer"].read_group(
            [
                ("property_id.state", "!=", "canceled"),
                ("property_type_id", "!=", False),
            ],
            ["ids:array_agg(id)", "property_type_id"],
            ["property_type_id"],
        )

        mapped_count = {
            d["property_type_id"][0]: d["property_type_id_count"] for d in data
        }
        mapped_ids = {d["property_type_id"][0]: d["ids"] for d in data}
        for record in self:

            record.offer_count = mapped_count.get(record.id, 0)
            record.offer_ids = mapped_ids.get(record.id, [])
