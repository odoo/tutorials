from odoo import models, fields

class EstatePropertyTags(models.Model):
    _name ="estate_property_tags"
    _description="property tags"
    _order="name asc"

    name = fields.Char(string ="Name", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('check_unique_name','UNIQUE(name)','The name of the tag should be unique'),
    ]
