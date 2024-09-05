from odoo import models, fields


class DentalTags(models.Model):
    _name = "dental.tags"

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)',
        'A tag with the same name already exists')
    ]
