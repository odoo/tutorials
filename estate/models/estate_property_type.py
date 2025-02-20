from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "name"
    _sql_constraints = [
        ("type_name_unique", "unique (name)", "The type name should be unique.")
    ]

    name = fields.Char("Property Type", required=True)
    sequence = fields.Integer(
        default=0, help="Used to order stages. Lower comes first."
    )
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
