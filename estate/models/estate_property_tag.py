from odoo import models, fields


class EstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "These are Estate Module Property Tags"

    name = fields.Char(string="Name", required=True)
