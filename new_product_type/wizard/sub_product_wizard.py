from odoo import models, fields

class SubProductWizard(models.TransientModel):
    _name = 'sub.product.wizard'
    _description = 'Sub Product Wizard'

    name = fields.Char(string="Sub Product Wizard", default="Sub Product Selection")
