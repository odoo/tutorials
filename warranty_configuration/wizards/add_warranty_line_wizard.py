from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class AddWarrantyLineWizard(models.TransientModel):
    _name = "add.warranty.line.wizard"
    _description = "Temporary line model for warranty in wizard"

    wizard_id = fields.Many2one(
        "add.warranty.wizard",
        string="Wizard Reference",
        readonly=True,
        required=True,
        ondelete='cascade',
    )

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        readonly=True,
        ondelete='cascade',
    )
    warranty_config_id = fields.Many2one("warranty.configuration", string="Year")
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)
    
    @api.depends("warranty_config_id")
    def _compute_end_date(self):
        today = date.today()
        for record in self:
            if record.warranty_config_id and record.warranty_config_id.year:
                record.end_date = today + relativedelta(
                    years=int(record.warranty_config_id.year)
                )
            else:
                record.product_id = record.product_id
                record.end_date = False
