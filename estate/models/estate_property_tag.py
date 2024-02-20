from odoo import fields, models


class EstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate tags."

    name = fields.Char(string="Name", required=True)
