from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate tag model"
    _order = "name"

    name = fields.Char(required=True)


    _check_unique_tag = models.Constraint("UNIQUE(name)", "tags should be unique")

