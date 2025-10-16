from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'property type must be unique.')]
    _order = "name"


    name = fields.Char(string='Property Type', required=True)
    property_ids = fields.One2many('estate.property', 'type_id', string="Properties")
    sequence = fields.Integer('Sequence', help="Used to order types. higher is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)