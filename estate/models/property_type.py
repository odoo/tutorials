from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "real.estate.property.type"
    _description = "Property Type"
    _order = "name"

    name = fields.Char(string="Property Type", required=True)
    description = fields.Text(string="Description")

    property_ids = fields.One2many(
        "estate_property", "property_type_id", string="Offers"
    )
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", store=True)
    sequence = fields.Integer("Sequence")
    offer_count = fields.Integer(compute="_compute_offer_count")
    _sql_constraints = [("name", "UNIQUE(name)", "A property type name must be unique")]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
