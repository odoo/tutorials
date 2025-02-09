from odoo import fields,models

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="estate property tag table"

    name = fields.Char('Tags', required=True)

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The property tag name must be unique.'),
    ]