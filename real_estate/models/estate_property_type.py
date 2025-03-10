from odoo import api, models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order="sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count=fields.Integer(string=" offers", compute="_compute_offer_count")
    sequence=fields.Integer("Sequence", default=1)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name should be unique.')
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)