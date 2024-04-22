from odoo import fields, models, api  # type: ignore


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "estate property type"
    _order = "sequence, name"

    name = fields.Char(string="Type", required=True)
    property_ids = fields.One2many("estate_property", "estate_property_type_id")
    offer_ids = fields.One2many("estate_property_offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer("Sequence", default=1)

    _sql_constraints = [
        ("unique_name", "unique(name)", "Choose another value - it has to be unique!")
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
