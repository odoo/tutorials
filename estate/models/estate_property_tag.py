from odoo import fields, models  # type: ignore


class EstatePropertyType(models.Model):
    _name = "estate_property_tag"
    _description = "estate property tag"

    name = fields.Char(string="Type", required=True)

    _sql_constraints = [
                     ('unique_name',
                      'unique(name)',
                      'Choose another value - it has to be unique!')
    ]
