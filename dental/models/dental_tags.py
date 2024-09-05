from odoo import fields, models
class Tags(models.Model):
    _name = "dental.tags"
    _description = "Tags for patients"

    name = fields.Char("Tag", required=True)