from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)
    tag_id = fields.Many2many(comodel_name="estate.property")
    _sql_constraints = [
        ('name_uniq', 'unique(name)',
        'A tag with the same name and applicability already exists.')
    ]
