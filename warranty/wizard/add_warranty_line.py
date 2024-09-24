from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class AddWarrantyLine(models.TransientModel):
    _name = 'add.warranty.line'

    product_template_id = fields.Many2one('product.template', string='Product')
    warranty_id = fields.Many2one('add.warranty', string='Wizard Reference')
    year = fields.Many2one('warranty.configuration')
    end_date = fields.Float()
    
    
    @api.onchange('year')
    def _onchange_end_date(self):
        if self.year :
            value=self.year
            self.end_date = date.today() + relativedelta(years=value.period)