from odoo import models, fields

class SaleOrder(models.Model):
    _inherit='sale.order'    
    
    print_in_report=fields.Boolean(string="Print in report?")
