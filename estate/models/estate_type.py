from odoo import fields, models

class EstateType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Type"

    name = fields.Char(string="Type", required=True)
    _name_idx = models.UniqueIndex('(name)', 'Another record already exists with the same name!')
