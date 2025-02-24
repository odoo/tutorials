from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real estate property tag for describe the property attributes (ex., renovated)"
    _order = 'name'
    # constraints
    _sql_constraints = [
      ('unique_tag', 'UNIQUE (name)', "The tag name must be unique.")
    ]

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
