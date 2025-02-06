from odoo import fields,models

class EstatePropertyTyags(models.Model):
    _name = "estate.property.tags"
    _description = "Property Tags"

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]
