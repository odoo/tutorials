from odoo import models, fields

class WarrantySelectionWizardLine(models.TransientModel):
    _name = 'warranty.selection.wizard.line'
    _description = 'Warranty Selection Wizard Line'

    wizard_id = fields.Many2one('warranty.selection.wizard', string="Warranty Selection Wizard")
    product_id = fields.Many2one('product.template', string="Product")
    warranty_id = fields.Many2one('warranty.configuration', string="Warranty")
    end_date = fields.Date(string="End Date")
    selected = fields.Boolean(string="Select", default=False)
