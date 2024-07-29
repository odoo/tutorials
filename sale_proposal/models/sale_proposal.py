from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

SALE_ORDER_STATE = [
    ('draft', "Draft"),
    ('sent', "Sent"),
    ('confirm', "Confirm"),
    ('cancel', "Cancelled"),
]


class SaleProposal(models.Model):
    _name = 'sale.proposal'
    _description = 'this is my model'

    name = fields.Char(string='Number', default='New', required=True, copy=False)
    proposal_status = fields.Selection([
        ('not_reviewed', ' Not Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Proposal Status', default='not_reviewed', copy=False, tracking=True, readonly=1)
    customer = fields.Many2one("res.partner", string="Customer", copy=False, required=True)
    quotation_template = fields.Many2one("sale.order.template", string="Quotation Template")
    expiration_date = fields.Date(string="Expiration Date", default=fields.Date.today() + relativedelta(months=1), copy=False)
    quotation_date = fields.Datetime(string="Quotation Date", default=fields.Datetime.now)
    payment_terms = fields.Many2one(
        comodel_name='account.payment.term',
        string="Payment Terms",
        store=True)
    order_ids = fields.One2many("sale.proposal.order", "order_id", string="Orders list")
    sale_order = fields.Char(string="Sale Order", readonly=1)
    sub_total = fields.Float(string="Subtotal")
    total = fields.Float(string="Total")
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

    def action_confirm_btn(self):
        return True

    @api.depends('state')
    def _compute_type_name(self):
        for record in self:
            if record.state in ('draft', 'sent', 'cancel'):
                record.type_name = _("Quotation")
            else:
                record.type_name = _("Sales Order")

    def action_quotation_send(self):
        if self.order_ids:
            self.state = 'sent'
        else:
            raise UserError('Please first add Products')

    def action_preview_sale_proposal(self):
        subtotal = 0
        total_with_tax = 0
        for record in self:
            for rec in record.order_ids:
                subtotal += rec.quantity * rec.unit_price
                total_with_tax += rec.subtotal
        self.sub_total = subtotal
        self.total = total_with_tax
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }

    def get_portal_url(self):
        url = f"/my/sale_proposal/{self.id}"
        return url
