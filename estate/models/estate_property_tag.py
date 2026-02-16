from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tags model"
    _check_name = models.Constraint("unique(name)", "Tag Name Must be UNIQUE")

    name = fields.Char("Name", required=True)
