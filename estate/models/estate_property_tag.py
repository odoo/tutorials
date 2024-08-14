from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property tag'
    name = fields.Char(required=True)
    color = fields.Integer()
    _order = 'name'
    _sql_constraints = [('name_uniq', 'unique (name)', "Tag name already exists!")]
