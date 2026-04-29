from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type"
    _order = "sequence desc, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    sequence = fields.Integer(default=1)
    count = fields.Integer(compute="_compute_count")

    _check_name = models.Constraint(
        "UNIQUE (name)",
        "Each type name must be unique",
    )

    @api.depends("offer_ids")
    def _compute_count(self):
        for record in self:
            record.count = len(record.offer_ids)
