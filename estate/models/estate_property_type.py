from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = 'name'

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", 'property_type_id')
    offer_ids = fields.One2many("estate.property.offer", 'property_type_id')
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer('Sequence', default=0)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property type name must be unique')
    ]
