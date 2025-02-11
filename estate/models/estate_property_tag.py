from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This is the model for the estate property tag"
    _order ="name"


    name = fields.Char(string="Name")
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ("unique_property_tag", "UNIQUE(name)", "The same property tag is already exist")
    ]
