from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"
    
    _sql_constraints = [
        ('unique_prop_tag', 'UNIQUE(name)','This property tag already exists.')
    ]

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer()
    