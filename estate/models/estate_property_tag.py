from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char("Tag", required=True)
    color = fields.Integer("Color Index", default=0)

    _check_unique_name = models.Constraint("unique(name)", "The name should be Unique")
