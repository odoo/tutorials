from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence asc, name"

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    name = fields.Char("Name", required=False)
    property_ids = fields.One2many("estate.property", "property_type_id", "Property")

    offer_ids = fields.One2many('estate.property.offer', inverse_name='property_type_id')
    offer_count = fields.Integer(string="Offer Count", default=0, compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'the property type name must be unique.')
    ]
