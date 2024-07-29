from odoo import models, fields, api


class SaleProposalLine(models.Model):
    _name = "sale.proposal.line"
    _description = "Sale Proposal Line"

    proposal_id = fields.Many2one(
        comodel_name='sale.proposal',
        string='Proposal Reference',
        required=True,
        ondelete='cascade',
        index=True,
        copy=False,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
    )
    product_uom_qty = fields.Float(
        string='Quantity',
        digits='Product Unit of Measure',
        required=True,
    )
    price_unit = fields.Float(
        string='Unit Price',
        required=True,
    )
    tax_id = fields.Many2many(
        comodel_name='account.tax',
        string='Taxes',
    )
    price_subtotal = fields.Integer(
        compute='_compute_price_subtotal',
        string='Subtotal',
        store=True,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='proposal_id.company_id.currency_id',
        store=True,
    )

    @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    def _compute_price_subtotal(self):
        for line in self:
            price = line.price_unit * line.product_uom_qty
            line.price_subtotal = price + (price * 0.15)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.list_price
