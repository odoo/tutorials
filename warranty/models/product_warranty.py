from odoo import models, fields, api


class ProductWarranty(models.Model):
    _name='product.warranty'
    
    name = fields.Char('Title')