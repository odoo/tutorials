from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute='_compute_offer_count')

    _unique_type_name = models.Constraint('UNIQUE(name)', "Type name must be unique")

    @api.depends('offer_count')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
