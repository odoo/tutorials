from odoo import api, models, fields
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

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

    name = fields.Char("Number", required=True, default=lambda self: _("New"))
    proposal_date = fields.Date("Proposal Date", default=fields.Date.today())
    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Status",
        default="draft",
    )
    company_id = fields.Many2one(
        comodel_name="res.company", default=lambda self: self.env.company
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
    )
    validity_date = fields.Date(
        string="Expiration",
        default=fields.Date.today() + relativedelta(months=1),
    )
    partner_invoice_id = fields.Many2one(
        comodel_name="res.partner",
        string="Invoice Address",
        compute="_compute_partner_invoice_id",
        store=True,
    )
    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string="Payment Terms",
        compute='_compute_payment_term_id',
        store=True, readonly=False, precompute=True, check_company=True,  # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    partner_shipping_id = fields.Many2one(
        comodel_name="res.partner",
        string="Delivery Address",
        compute="_compute_partner_shipping_id",
        store=True,
    )
    order_line = fields.One2many(
        comodel_name='sale.proposal.line',
        inverse_name='proposal_id',
        string='Order Lines',
        copy=True,
        readonly=False,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
    )
    team_id = fields.Many2one(
        comodel_name='crm.team',
        string='Sales Team',
        change_default=True,
        default=lambda self: self.env['crm.team']._get_default_team_id(),
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    proposal_status = fields.Selection(
        selection=PROPOSAL_STATUS,
        string="Proposal Status",
        default="not_reviewed",
        readonly=True,
    )
    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sale Order",
        readonly=True,
    )

    @api.depends('partner_id')
    def _compute_partner_invoice_id(self):
        for order in self:
            order.partner_invoice_id = order.partner_id.address_get(['invoice'])['invoice'] if order.partner_id else False

    @api.depends('partner_id')
    def _compute_partner_shipping_id(self):
        for order in self:
            order.partner_shipping_id = order.partner_id.address_get(['delivery'])['delivery'] if order.partner_id else False

    @api.depends('partner_id')
    def _compute_payment_term_id(self):
        for order in self:
            order = order.with_company(order.company_id)
            order.payment_term_id = order.partner_id.property_payment_term_id

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

    def action_preview_sale_proposal(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }

    def get_portal_url(self):
        url = f"/my/proposals/{self.id}"
        return url

    def action_confirm(self):
        self.state = 'confirm'
