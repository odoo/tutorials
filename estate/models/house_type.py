from odoo import api, fields, models

class house_type(models.Model):
    _name = 'estate.house_type'
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'type name value is already exisiting')
    ]
    _order = 'name'

    name = fields.Char(required=True)
    houses_ids = fields.One2many('house', 'house_type_id')
    sequence = fields.Integer(default=1)
    offers_count = fields.Integer(compute="_compute_offers_count")

    @api.depends("houses_ids.offers_ids")
    def _compute_offers_count(self):
        for house_type in self:
            house_type.offers_count = len(house_type.houses_ids.offers_ids)

