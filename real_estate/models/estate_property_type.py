from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence,name"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offers")

    @api.depends("offer_ids")
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ("unique_property_type_name", "unique(name)", "Property Type already exists.")
    ]
