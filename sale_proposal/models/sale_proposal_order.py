from odoo import api, fields, models


class SalePropodalOrder(models.Model):
    _name = "sale.proposal.order"
    _description = "Sale Proposal Order Model"
    _order = "product"

    order_id = fields.Many2one("sale.proposal", string="Order", required=True)
    product = fields.Many2one("product.product", string="Product")
    description = fields.Text(string="Description", required=True)
    quantity = fields.Integer(string="Quantity", required=True)
    product_uom = fields.Char(string="UoM", required=True, default="Number")
    unit_price = fields.Float(string="Unit Price", required=True, compute="_compute_unit_price")
    tax_id = fields.Char(string="Taxes", default="15%", readonly=True)
    subtotal = fields.Float(string="Subtotal", readonly=True, compute="_compute_subtotal")

    @api.depends('quantity', 'unit_price', 'subtotal')
    def _compute_subtotal(self):
        for record in self:
            if record.quantity > 0:
                amount = record.quantity * record.unit_price
                record.subtotal = amount + (amount * .15)
            else:
                record.subtotal = 0.0

    @api.depends('product')
    def _compute_unit_price(self):
        for record in self:
            if record.product:
                record.unit_price = record.product.lst_price
                record.quantity = 1
            else:
                record.unit_price = 0.0
