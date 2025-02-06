from odoo import fields,models

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="estate property tag table"

    name = fields.Char('Tags', required=True)