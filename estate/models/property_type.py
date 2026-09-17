from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence asc"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer(default=1, help="Used to order type. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _name_uniq = models.Constraint(
        "UNIQUE (name)",
        "The name of the type must be unique!",
    )

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
