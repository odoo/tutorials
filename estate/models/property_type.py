from odoo import api, fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "describes the type of a property"
    _order = "sequence,name"
    _sql_constraints = [('name_unique', 'unique(name)', 'A property type name must be unique')]

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer('Sequence', default=1)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
