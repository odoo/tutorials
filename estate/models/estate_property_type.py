from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char("Name", required=True)

    # SQL Constarint
    _check_name = models.Constraint('unique(name)', "The name must be unique")
