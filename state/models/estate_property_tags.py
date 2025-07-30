from odoo import fields, models

class PropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Tags to describe real estate properties"
    _order = "name"

    name = fields.Char('Title', required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('unique_name','UNIQUE(name)','The Tag must be UNIQUE.')
    ]