from odoo import fields, models


class EstateProperties(models.Model):
    _name = "estate.property.tag"
    _description = " Estate Property Tags"
    _order = "name"

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('check_tag_name', 'UNIQUE(name)',
         'The property tag must be unique!!')
    ]
