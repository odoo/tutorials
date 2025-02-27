from odoo import models,fields


class WarrantyYear(models.Model):
    _name = "warranty.year"
    _description = "Warranty year"

    name = fields.Char(string="Warranty Duration",required=True)
    years = fields.Integer(string = "Years",required=True)