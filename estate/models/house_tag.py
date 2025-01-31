from odoo import fields, models

class HouseTag(models.Model):
    _name = 'estate.house.tag'
    _description = 'House Tag Model'
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'tag name value is already existing')
    ]
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()
