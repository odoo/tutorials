from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of properties available in the estate module."
    _order = "name"

    name = fields.Char('Name', required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Property")
    sequence = fields.Integer("Sequence", default=1, help="Used to order types. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="compute_offer_count", string="Offers Count", store=True, readonly=True)

    _sql_constraints = [
        ('check_property_type_name', 'UNIQUE(name)', 'A Type must be unique.'),
    ]


    @api.depends('offer_ids')
    def compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
