from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tag'
    _order = "name asc"

    _tag_name_uniq = (models.Constraint("""UNIQUE (name)""",
             "The tag name must be unique."))

    name = fields.Char('Title', required=True, translate=True)
    color = fields.Integer('Color')
