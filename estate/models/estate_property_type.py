from odoo import api, fields, models

class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "Property type models file"

    name = fields.Char("Name", required=True)

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The name should be unique')
    ]

    _order = "name"

    property_id = fields.One2many("estate.property", "property_type_id")
    offer_counts = fields.Integer(compute="_compute_offer_count")

    @api.depends("property_id.offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_counts = sum(len(prop.offer_ids) for prop in record.property_id)
