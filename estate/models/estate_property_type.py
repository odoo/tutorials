from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type, i.e. type of the building accourding to the use"

    name = fields.Char(required=True)
    _check_name = models.Constraint(
            'unique (name)',
            'The property type name must be unique, choose different name')
    description = fields.Text(help="Description of thus estate property type for better user understanding")
    code = fields.Char(required=True, help="Single to double character code for identification when space is scarce")
    _check_code = models.Constraint(
            'unique (code)',
            'The property type code must be unique, choose different code')
