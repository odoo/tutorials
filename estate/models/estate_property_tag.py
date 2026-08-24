from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag, i.e. simple boolean characteristics of the estate outside the normal properties"

    name = fields.Char(required=True)
    _check_name = models.Constraint(
            'unique (name)',
            'The property tag name must be unique, choose different name')
    visual_code = fields.Char(required=True, help="Visual character for purpose of brief visualization")
    _check_visual_code = models.Constraint(
            'unique (visual_code)',
            'The property tag visual code must be unique, choose different code')
