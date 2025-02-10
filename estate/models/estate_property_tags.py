from odoo import fields,models

class EstatePropertyTyags(models.Model):
    _name = "estate.property.tags"
    _description = "Property Tags"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color Index")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]
