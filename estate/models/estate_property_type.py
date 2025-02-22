from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"

    name = fields.Char("Property Type", required=True)
    property_type_ids = fields.One2many("estate.property", "property_type_id", string="Related Properties")
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer("Number of offers", compute="_compute_offer_count")

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The Type name should be unique')
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
