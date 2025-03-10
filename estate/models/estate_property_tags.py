from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tags"
    _description = "Property Tags"
    _order = "name desc"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('unique_name_tags','UNIQUE(name)','Property Tags should be unique')
    ]
    