from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"

    name = fields.Char("Tage Name", required=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The name of the Tag should be unique')
    ]
