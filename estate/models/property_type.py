from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"
    _order = "name"

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _name_idx = models.UniqueIndex('(name)', 'Another record already exists with the same name!')

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
