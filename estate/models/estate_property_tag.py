from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag of estate"
    _sql_constrains = [
        ('check_name', 'UNIQUE(name)',
         'Tag name has to be unique')
    ]
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()
