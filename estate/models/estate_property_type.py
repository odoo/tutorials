from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Specific types of properties"
    _order = "name desc"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id', string="Property")
    sequence = fields.Integer(string='Sequence', default=1)
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id')
    offer_count = fields.Integer(string="Offers", compute="_compute_count_offers")

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property type already created')
    ]

    @api.depends('offer_ids')
    def _compute_count_offers(self):
        for records in self:
            records.offer_count = len(records.offer_ids)
