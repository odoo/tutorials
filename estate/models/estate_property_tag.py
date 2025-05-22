from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "ch7 exercise tutorial"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(name)',
         'Each property tag should have a unique name.')
    ]