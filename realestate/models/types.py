from odoo import api, fields, models


class Types(models.Model):
    _name = "types"
    _order = "sequence"
    name = fields.Char(required=True)
    properties_ids = fields.One2many("realestate", "type_id")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many("offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        (
            "unique_name",
            "unique(name)",
            "Name already exists",
        ),
    ]
