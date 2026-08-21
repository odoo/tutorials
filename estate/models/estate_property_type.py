from odoo import models, fields, api
from odoo.orm.fields_relational import One2many


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of estate property"
    _order = "name"
    name = fields.Char(string="Name", required=True)
    property_ids = One2many("estate.property", "property_type_id", "properties")
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many("estate.property.offers", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    _check_property_type = models.Constraint(
        "UNIQUE(name)",
        "Property type must be unique",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
