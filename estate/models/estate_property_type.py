from odoo import api, fields, models  # ty: ignore[unresolved-import]


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property for real estate"
    _order = "sequence, name"

    name = fields.Char(required=True)
    _check_name = models.Constraint("UNIQUE(name)", "Type names must be unique")
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
