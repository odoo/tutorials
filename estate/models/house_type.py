from odoo import api, fields, models

class HouseType(models.Model):
    _name = 'estate.house.type'
    _description = 'House Type Model'
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'type name value is already existing')
    ]
    _order = 'name'

    name = fields.Char(required=True)
    house_ids = fields.One2many('estate.house', 'house_type_id')
    sequence = fields.Integer(default=1)
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("house_ids.offer_ids")
    def _compute_offer_count(self):
        for house_type in self:
            house_type.offer_count = len(house_type.house_ids.offer_ids)
