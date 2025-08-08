from odoo import models, fields, api, timedelta


class AddWarrantyWizardLine(models.TransientModel):
    _name = "add.warranty.wizard.line"
    _description = 'Add Warranty Wizard Line'

    wizard_id = fields.Many2one("add.warranty.wizard")
    product_id = fields.Many2one("product.product", string="Product")
    year_id = fields.Many2one("warranty.year", string="Year")
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)
    add = fields.Boolean(default=False)

    @api.depends("year_id")
    def _compute_end_date(self):
        for line in self:
            if line.year_id:
                line.end_date = fields.Date.today() + timedelta(days=365 * line.year_id.year)
