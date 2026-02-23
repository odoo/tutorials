from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tags model"
    _order = "name"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _check_name = models.Constraint("unique(name)", "Tag Name Must be UNIQUE")
