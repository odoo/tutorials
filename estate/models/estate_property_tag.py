from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag"
    _order = 'name'

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')
    property_ids = fields.Many2many("estate.property", string="Properties")

    _check_name_uniq = models.Constraint(
        'UNIQUE (name)',
        "This tag already exists.",
    )
