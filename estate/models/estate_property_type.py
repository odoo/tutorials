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
    offer_id = fields.One2many("estate.property.offer", "property_id")
    offer_counts = fields.Integer(compute="_compute_offer_counts")

    @api.depends("offer_id")
    def _compute_offer_counts(self):
        for record in self:
            record.offer_counts = len(record.offer_id)
