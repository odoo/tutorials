from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tag'

    name = fields.Char('Title', required=True, translate=True)

    _tag_name_uniq = (models.Constraint("""UNIQUE (name)""",
             "The tag name must be unique."))
