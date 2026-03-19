from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(string="Name", required=True)

    _check_name = models.Constraint("UNIQUE(name)", "Name must be unique.")
