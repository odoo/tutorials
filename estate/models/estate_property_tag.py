from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag"

    name = fields.Char('Name', required=True)
    property_ids = fields.Many2many("estate.property", string="Properties")

    _check_name_uniq = models.Constraint(
        'UNIQUE (name)',
        "This tag already exists.",
    )
