from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate system - Property Tag"

    _unique_tag_name = models.Constraint(
        'UNIQUE(name)',
        'The Property Tag name has to be Unique.'
    )

    name = fields.Char(string="Tag Name", required=True)
