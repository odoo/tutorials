from odoo import fields, models  # type: ignore


class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "estate property tag"
    _order = "name"

    name = fields.Char(string="Type", required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
                     ('unique_name',
                      'unique(name)',
                      'Choose another value - it has to be unique!')
    ]
