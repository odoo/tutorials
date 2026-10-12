from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Different Tags for Property"
    _order = "name"

    name = fields.Char("Tag")
    color = fields.Integer("Color Index")
    _check_tag_name = models.Constraint("unique(name)", "Tag name should be unique")
