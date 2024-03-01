from odoo import fields, models, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate type"
    _order = "sequence, name"

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "A property Type must be unique."),
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    sequence = fields.Integer(
        string="Sequence", default=1, help="Used to order stages. Lower is better."
    )
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_count_offers")

    @api.depends("offer_ids")
    def _count_offers(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
