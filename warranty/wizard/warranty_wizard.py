from odoo import models, fields, api

class WarrantyProductWizard(models.TransientModel):
    _name = 'warranty.product.wizard'
    _description = 'Warranty Product Wizard'

    product_id = fields.One2many("")
    year = fields.Many2one(comodel_name="warranty")
    end_date = fields.Date(readonly=True, compute="_compute_end_date");


    @api.depends("year")
    def _compute_end_date(self):
        pass
