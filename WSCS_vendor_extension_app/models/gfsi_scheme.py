from odoo import models, fields


class GFSIScheme(models.Model):
    _name = "gfsi.scheme"
    _description = "GFSI Schemes"

    name = fields.Char(string="Scheme Name")
