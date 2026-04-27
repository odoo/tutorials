from odoo import models, fields, api


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence'

    name = fields.Char(string="Type", required=True)
    sequence = fields.Integer()
    properties_id = fields.One2many(comodel_name="estate.property", inverse_name="type_id")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _check_name = models.Constraint(
        'unique(name)', "The property type name should be unique"
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
