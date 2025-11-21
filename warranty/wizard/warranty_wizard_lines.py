from odoo import fields, models, api, _
import re

class WarrantyWizardLines(models.TransientModel):
    _name = 'warranty.wizard.lines'
    _description = 'Products for wizard lines'

    wizard_id = fields.Many2one('warranty.add.warranty', string="Warranty Selection Wizard")
    quantity = fields.Float(string="Quantity")
    product_id = fields.Many2one('product.template', string="Product")
    year = fields.Many2one('warranty.configuration', string="Warranty")
    end_date = fields.Date(compute="_compute_end_date")

    def get_year_number(self):
        match = re.search(r'(\d+)', str(self.year.name))
        return int(match.group(1)) if match else 0

    @api.depends("year.name")
    def _compute_end_date(self):
        for record in self:
            record.end_date = fields.Date.add(fields.Date.today(), years=record.get_year_number())
            