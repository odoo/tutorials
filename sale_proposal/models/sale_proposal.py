from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import UserError


SALE_ORDER_STATE = [
    ('draft', "Draft"),
    ('sent', "Sent"),
    ('confirm', "Confirm"),
]


class SaleProposal(models.Model):
    _name = 'sale.proposal'
    _description = 'this is my model'

    name = fields.Char(string='Number', default='New', required=True, copy=False, readonly=True)
    is_proposal = fields.Boolean(string="Is Proposal")
    proposal_status = fields.Selection([
        ('not_reviewed', ' Not Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Proposal Status', default='not_reviewed', copy=False)
    sales_order = fields.Char(string="Sale order", readonly=True)
    customer = fields.Many2one("res.partner", string="Customer", copy=False, required=True)
    quotation_template = fields.Many2one(
        "sale.order.template", string="Quotation Template")
    expiration_date = fields.Date(string="Expiration", default=fields.Date.today() + relativedelta(months=1), copy=False)
    quotation_date = fields.Datetime(string="Quotation Date", default=datetime.now())
    payment_terms = fields.Many2one('account.payment.term', string="Payment Terms")
    order_ids = fields.One2many("sale.proposal.order", "order_id", string="Orders list")

    # Lines and line based computes
    order_line = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='order_id',
        string="Order Lines",
        copy=True, auto_join=True)

    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    type_name = fields.Char(string="Type Name", compute='_compute_type_name')

    @api.depends('state')
    def _compute_type_name(self):
        for record in self:
            if record.state in ('draft', 'sent', 'cancel'):
                record.type_name = ("Quotation")
            else:
                record.type_name = ("Sales Order")

    def action_quotation_send(self):
        if self.order_ids:
            self.state = "sent"

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals.get('name') == ('New'):
            cur_yr = fields.Date.today().strftime('%Y')
            cur_mth = fields.Date.today().strftime('%b')
            seq_code = 'sale.proposal'
            sequence = self.env['ir.sequence'].next_by_code(seq_code)
            vals['name'] = f'Proposal/{cur_yr}/{cur_mth}/{sequence}'
        res = super().create(vals)
        return res

    def action_send_mail(self):
        template_id = self.env.ref('email_template_proposal').id
        template = self.env['mail.template'].browse(template_id)
        if not template:
            raise UserError("Email template not found!")
        for record in self:
            template.send_mail(record.id, template_id, force_send=True)
        self.state = 'sent'

    def action_confirm(self):
        return True

    def get_portal_url(self):
        url = f"/my/sale_proposal/{self.id}"
        return url

    def action_preview_sale_proposal(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }
