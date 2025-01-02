from odoo import api, fields, models
from datetime import date, timedelta

class WarrantyConfiguration(models.Model):
    _name = 'warranty.configuration'
    _description = 'Product warranty Configuration'

    name= fields.Char(required=True)
    warranty_product=fields.Many2one('product.template')
    year=fields.Integer(required=True)
    percentage=fields.Float(required=True)
    end_date=fields.Date(copy= False, compute="_compute_end_date", store=True, readonly=True)

    _sql_constraints = [('check_unique_year', 'UNIQUE(year)', 'Warranty year must be unique.')]

    @api.depends('year')
    def _compute_end_date(self):
        for record in self:
            if record.year:
                record.end_date = date.today() + timedelta(days=record.year * 365)
            else:
                record.end_date = False
