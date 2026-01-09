from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name, sequence'

    name = fields.Char(required=True)
    sequence = fields.Integer()
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    # Depends Decorator
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # SQL Constarint
    _check_name = models.Constraint('unique(name)', "The name must be unique")

    # For Inline View
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties")
