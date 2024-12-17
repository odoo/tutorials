from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Table"

    name = fields.Char("Name", required=True, unique=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(
        "Offer Count",
        compute="_compute_offer_count",
    )
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The property type must be unique.")
    ]
    _order = "sequence, name"

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
