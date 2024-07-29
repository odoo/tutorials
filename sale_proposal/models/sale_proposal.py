from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


SALE_ORDER_STATE = [
    ("draft", "Draft"),
    ("sent", "Sent"),
    ("confirm", "Confirm"),
]
PROPOSAL_STATUS = [
    ("not_reviewed", "Not Reviewed"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
]


class SaleProposal(models.Model):
    _name = "sale.proposal"
    _description = "Sale Proposal"

    name = fields.Char("Number", default=lambda self: _('New'))
    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Status",
        default="draft",
    )

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            cur_yr = fields.Date.today().strftime('%Y')
            cur_mth = fields.Date.today().strftime('%b')
            seq_code = 'sale.proposal'
            sequence = self.env['ir.sequence'].next_by_code(seq_code)
            vals['name'] = f'Proposal/{cur_yr}/{cur_mth}/{sequence}'
        res = super().create(vals)
        return res

    def unlink(self):
        for proposal in self:
            # Unlink related sale orders if needed
            proposal.sale_order_id.unlink()
        return super().unlink()

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
    )
    validity_date = fields.Date(
        string="Expiration",
    )
    partner_invoice_id = fields.Many2one(
        comodel_name="res.partner",
        string="Invoice Address",
        compute="_compute_partner_invoice_id",
        store=True,
    )
    partner_shipping_id = fields.Many2one(
        comodel_name="res.partner",
        string="Delivery Address",
        compute="_compute_partner_shipping_id",
        store=True,
    )

    @api.depends('partner_id')
    def _compute_partner_invoice_id(self):
        for order in self:
            order.partner_invoice_id = order.partner_id.address_get(['invoice'])['invoice'] if order.partner_id else False

    @api.depends('partner_id')
    def _compute_partner_shipping_id(self):
        for order in self:
            order.partner_shipping_id = order.partner_id.address_get(['delivery'])['delivery'] if order.partner_id else False

    payment_term_id = fields.Many2one(
        comodel_name="account.payment.term",
        string="Payment Terms",
        compute="_compute_payment_term_id",
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    @api.depends('partner_id')
    def _compute_payment_term_id(self):
        for order in self:
            order = order.with_company(order.company_id)
            order.payment_term_id = order.partner_id.property_payment_term_id

    order_line = fields.One2many(
        comodel_name='sale.proposal.line',
        inverse_name='proposal_id',
        string="Order Lines",
        copy=True, auto_join=True)

    proposal_status = fields.Selection(
        selection=PROPOSAL_STATUS,
        string="Proposal Status",
        default="not_reviewed",
        readonly=True,
    )
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Proposal',
        readonly=True,
    )

    def action_send_by_email(self):
        template_id = self.env.ref('sale.email_template_edi_sale').id
        template = self.env['mail.template'].browse(template_id)
        if template:
            template.send_mail(self.id, force_send=True)
        self.state = 'sent'

    def action_confirm(self):
        if self.state != 'confirm':
            raise UserError(_('not being confrim'))
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'order_line': [(0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.price_unit,
            }) for line in self.order_line],

        })
        sale_order.action_confirm()
        self.sale_order_id = sale_order.id
        self.state = 'confirm'

    def get_portal_url(self):
        self.ensure_one()
        return f'/my/sale_proposal/{self.id}'

    def action_preview_sale_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }
