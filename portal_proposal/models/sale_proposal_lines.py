from odoo import fields, models, api


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
        required=True,
        default=1,
    )
    price_unit = fields.Float(
        string='Unit Price',
        required=True,
        compute="_compute_product_price",
    )
    tax_id = fields.Char(
        string='Taxes',
        default="5%",
    )
    price_subtotal = fields.Monetary(
        compute='_compute_price_subtotal',
        string='Subtotal',
        store=True,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='proposal_id.company_id.currency_id',
        store=True,
    )
    order_id = fields.Many2one('sale.order', string="Order Reference", ondelete='cascade')

    @api.depends('product_id')
    def _compute_product_price(self):
        for line in self:
            if line.product_id:
                line.price_unit = line.product_id.lst_price
            else:
                line.price_unit = 0.00

    @api.depends('price_unit', 'tax_id', 'product_uom_qty')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = (line.product_uom_qty * line.price_unit) + ((line.product_uom_qty * line.price_unit) * 0.05)
