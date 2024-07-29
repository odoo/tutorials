from odoo import fields, models, api


class SaleProposalOrder(models.Model):
    _name = "sale.proposal.order"
    _description = "Sale Proposal Order Model"

    order_id = fields.Many2one("sale.proposal", string="Order", required=True)
    product = fields.Many2one("product.product", string="Product")
    description = fields.Text(string="Description", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    unit_price = fields.Float(string="Unit Price", required=True, compute="_compute_unit_price")
    tax_id = fields.Char(string="Taxes", default="15%")
    sub_total = fields.Float(string="Subtotal", readonly=True, compute="_compute_subtotal")
    product_uom = fields.Char(string="Uom")

    @api.depends('quantity', 'unit_price', 'sub_total')
    def _compute_subtotal(self):
        for record in self:
            if record.quantity > 0:
                amount = record.quantity * record.unit_price
                record.sub_total = amount * .15 + amount
            else:
                record.sub_total = 0.0

    @api.depends('product')
    def _compute_unit_price(self):
        for record in self:
            if record.product:
                record.unit_price = record.product.lst_price
                record.quantity = 1
            else:
                record.unit_price = 0.0
