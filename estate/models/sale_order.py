from odoo import api, fields, models


SALE_ORDER_STATE = [
    ('draft', "Draft"),
    ('sent', "Send"),
    ('sale', "Confirm"),
    ('cancel', "Cancelled"),
]


class EstatePropertySalesOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    proposal_number = fields.Char(string="Proposal Number", readonly=True, copy=False)
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", readonly=True, copy=False)

    @api.model
    def create(self, vals):
        if vals.get('proposal_number', 'New') == 'New':
            vals['proposal_number'] = self.env['ir.sequence'].next_by_code('sale.order') or '/'
        return super().create(vals)
