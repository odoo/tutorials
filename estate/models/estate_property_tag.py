from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This contains various tags."

    name = fields.Char(string = "Tag Name", required = True)
