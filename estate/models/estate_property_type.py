from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "My Estate Property Type"
    _order = "name"

    name = fields.Char(required = True, string = "Name")
    property_ids = fields.One2many("estate.property", "property_type_id", string = "Property")
    sequence = fields.Integer("Sequence", default = 1, help = "Used to order.")

    offer_ids = fields.One2many(related = "property_ids.offer")
    offer_count = fields.Integer(compute = "_compute_count")

    _sql_constraints = [
        ("unique_name", "unique(name)", "Property type should be unique.")
    ]

    @api.depends("offer_ids")
    def _compute_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
