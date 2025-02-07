from odoo import models, fields


class EstateTag(models.Model):
    _name = "estate.property.tag"

    name = fields.Char(string="Name", required=True)
    