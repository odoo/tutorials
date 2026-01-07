from odoo import fields, models


class RealEstateTag(models.Model):
    _name = 'real.estate.tag'
    _description = 'Real Estate Tag'

    name = fields.Char(required=True)
    _unique_tag_name = models.Constraint(
        'UNIQUE(name)',
        'The property tag name must be unique.',
    )
