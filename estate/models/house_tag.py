from odoo import fields, models

class house_tag(models.Model):
    _name = 'estate.house_tag'
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'tag name value is already exisiting')
    ]

    name = fields.Char(required=True)
    