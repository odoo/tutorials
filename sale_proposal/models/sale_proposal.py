from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError, UserError

SALE_ORDER_STATE = [
    ('draft', "Draft"),
    ('sent', "Send"),
    ('sale', "Confirm"),
]
PROPOSAL_STATUS = [
    ('not_reviewed', "Not Reviewed"),
    ('approved', "Approved"),
    ('rejected', "Rejected")
]


class SaleProposal(models.Model):
    _name = 'sale.proposal'
    _description = 'Sale Proposal'

    number = fields.Char(string="Number", required=True, copy=False, default=lambda self: _('New'))
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    user_id = fields.Many2one(comodel_name='res.users', string='Salesperson', default=lambda self: self.env.user)
    team_id = fields.Many2one(comodel_name='crm.team', string='Sales Team', change_default=True, default=lambda self: self.env['crm.team']._get_default_team_id(), domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    state = fields.Selection(selection=SALE_ORDER_STATE, string="Status", default='draft', copy=False)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)
    validity_date = fields.Date(string="Expiration")
    partner_invoice_id = fields.Many2one(comodel_name="res.partner", string="Invoice Address", compute="_compute_partner_invoice_id", store=True)
    partner_shipping_id = fields.Many2one(comodel_name="res.partner", string="Delivery Address", compute="_compute_partner_shipping_id", store=True)
    order_line = fields.One2many(comodel_name='sale.proposal.line', inverse_name='proposal_id', string="Order Lines", copy=True, auto_join=True, ondelete='cascade')
    payment_term_id = fields.Many2one(comodel_name='account.payment.term', string="Payment Terms", compute='_compute_payment_term_id', store=True, readonly=False, precompute=True, check_company=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    proposal_status = fields.Selection(selection=PROPOSAL_STATUS, string="Proposal Status", default='not_reviewed', readonly=True)
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", readonly=True)
    sale_proposal_line = fields.One2many(comodel_name='sale.proposal.line', inverse_name='proposal_id', copy=True, auto_join=True)
    street = fields.Char(related='partner_id.street', readonly=True)
    street2 = fields.Char(related='partner_id.street2', readonly=True)
    city = fields.Char(related='partner_id.city', readonly=True)
    state_id = fields.Many2one('res.country.state', related='partner_id.state_id', readonly=True)
    zip = fields.Char(related='partner_id.zip', readonly=True)
    country_id = fields.Many2one('res.country', related='partner_id.country_id', readonly=True)
    full_address = fields.Char(compute='_compute_full_address', readonly=True)

    @api.depends('street', 'street2', 'city', 'state_id', 'zip', 'country_id')
    def _compute_full_address(self):
        for record in self:
            address_parts = [
                record.street or '',
                record.street2 or '',
                record.city or '',
                record.state_id.name if record.state_id else '',
                record.zip or '',
                record.country_id.name if record.country_id else ''
            ]
            record.full_address = '\n'.join(filter(None, address_parts))

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

    @api.depends('partner_id')
    def _compute_payment_term_id(self):
        for order in self:
            order = order.with_company(order.company_id)
            order.payment_term_id = order.partner_id.property_payment_term_id

    @api.model
    def create(self, vals):
        if vals.get('number', _('New')) == _('New'):
            current_year = fields.Date.today().strftime('%Y')
            current_month = fields.Date.today().strftime('%b')
            seq_code = 'sale.proposal'
            sequence = self.env['ir.sequence'].next_by_code(seq_code)
            vals['number'] = f'Proposal/{current_year}/{current_month}/{sequence}'
        result = super().create(vals)
        return result

    def action_quotation_send(self):
        if self.state not in ['draft', 'sent']:
            raise UserError(_("You can only send quotations that are in draft or sent state."))
        self.state = 'sent'

    def action_confirm(self):
        if not self.order_line:
            raise ValidationError(_("You cannot confirm a proposal without order lines."))

        sale_order = self.env["sale.order"].create({
            "partner_id": self.partner_id.id,
            "order_line": [(0, 0, {
                "product_id": line.product_id.id,
                "product_uom_qty": line.product_uom_qty,
                "price_unit": line.price_unit,
            }) for line in self.order_line],
        })
        sale_order.action_confirm()
        self.sale_order_id = sale_order.id
        self.state = 'sale'

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
