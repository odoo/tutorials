from odoo import models, fields


class GFSICertificate(models.Model):
    _name = "gfsi.certificate"
    _description = "GFSI Certifcate"

    name = fields.Char(string="Certification Name")
