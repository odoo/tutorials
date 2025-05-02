from odoo import api, fields, models


class Types(models.Model):
    _name = "realestate_types"
    _order = "sequence"
    _description = "Types"
    name = fields.Char(required=True)
    properties_ids = fields.One2many("realestate_property", "type_id")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many("realestate_offer", "property_type_id")
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
