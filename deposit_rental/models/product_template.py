from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    current_company_id = fields.Many2one(
        "res.company",
        string="Current Company",
        compute="_compute_current_company",
        store=False,
    )    
    require_deposit = fields.Boolean(string="Require Deposit")

    deposit_product_id = fields.Many2one(
        "product.product",
        string="Deposit Product",
        related="current_company_id.deposit_product_id",  
        readonly=False,
    )
    deposit_amount = fields.Float(
        string="Deposit Amount",
        related="deposit_product_id.lst_price",
        readonly=True,
    )

    @api.depends_context("company")
    def _compute_current_company(self):
        """Ensure company updates when switching."""
        for product in self:
            product.current_company_id = self.env.company
