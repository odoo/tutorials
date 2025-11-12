from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate property tag for describe the property attributes"
    _order = 'name'
    _sql_constraints = [('unique_tag_name','UNIQUE(name)',"The property tag name must be unique!")]

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="color")
