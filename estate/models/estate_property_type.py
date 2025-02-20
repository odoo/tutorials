from odoo import models, fields, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of Property"
    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name)", "The name of a property type must not already exist"),
    ]
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
