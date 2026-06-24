from odoo import _, fields, models


class AwesomeEstatePropertyType(models.Model):
    _name = 'awesome.estate.property.type'
    _description = "Real Estate Property Type"
    _order = 'name'

    name = fields.Char(required=True)

    # -----------------------------------------------------------------------
    # SQL Constraints
    # -----------------------------------------------------------------------
    _check_type_name_unique = models.Constraint(
        'UNIQUE(name)',
        _('The property type name must be unique.'),
    )
