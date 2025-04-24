from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "property type"
    _order = "sequence, name, id"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate_property", "estate_property_type", string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    
    offer_ids = fields.One2many(comodel_name='estate_property_offer', inverse_name='property_type_id', string="Related offers")
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
