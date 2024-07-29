from odoo import api, models, fields
from odoo.tools.translate import _
from odoo.exceptions import UserError


SALE_ORDER_STATE = [
    ("draft", "Draft"),
    ("sent", "Sent"),
    ("confirm", "Confirm"),
    ("cancel", "Cancelled"),
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
    payment_term_id = fields.Many2one(
        comodel_name="account.payment.term",
        string="Payment Terms",
        compute="_compute_payment_term_id",
        store=True,
        readonly=False,
        precompute=True,
        check_company=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    order_line = fields.One2many(
        comodel_name="sale.proposal.line",
        inverse_name="proposal_id",
        string="Order Lines",
        copy=True,
        readonly=False,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    team_id = fields.Many2one(
        comodel_name="crm.team",
        string="Sales Team",
        change_default=True,
        default=lambda self: self.env["crm.team"]._get_default_team_id(),
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
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="company_id.currency_id",
        store=True,
    )
    amount_total = fields.Monetary(
        string="Total Amount", compute="_compute_amount_total", store=True
    )

    @api.depends("order_line.price_subtotal")
    def _compute_amount_total(self):
        for proposal in self:
            proposal.amount_total = sum(
                line.price_subtotal for line in proposal.order_line
            )

    @api.depends("partner_id")
    def _compute_partner_invoice_id(self):
        for order in self:
            order.partner_invoice_id = (
                order.partner_id.address_get(["invoice"])["invoice"]
                if order.partner_id
                else False
            )

    @api.depends("partner_id")
    def _compute_partner_shipping_id(self):
        for order in self:
            order.partner_shipping_id = (
                order.partner_id.address_get(["delivery"])["delivery"]
                if order.partner_id
                else False
            )

    @api.depends("partner_id")
    def _compute_payment_term_id(self):
        for order in self:
            order = order.with_company(order.company_id)
            order.payment_term_id = order.partner_id.property_payment_term_id

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            cur_yr = fields.Date.today().strftime("%Y")
            cur_mth = fields.Date.today().strftime("%b")
            seq_code = "sale.proposal"
            sequence = self.env["ir.sequence"].next_by_code(seq_code)
            vals["name"] = f"Proposal/{cur_yr}/{cur_mth}/{sequence}"
        res = super().create(vals)
        return res

    def _find_mail_template(self):

        self.ensure_one()
        if self.env.context.get("proforma") or self.state != "confirm":
            return self.env.ref(
                "portal_proposal.mail_template_sale_proposal", raise_if_not_found=False
            )
        else:
            return self._get_confirmation_template()

    def action_quotation_send(self):
        self.ensure_one()

        # Fetch the mail template
        mail_template = self._find_mail_template()

        # Prepare context for email composition
        ctx = {
            "default_model": "sale.proposal",
            "default_res_id": self.id,
            "default_template_id": mail_template.id if mail_template else None,
            "default_composition_mode": "comment",
            "mark_so_as_sent": True,
            "default_email_layout_xmlid": "mail.mail_notification_layout_with_responsible_signature",
            "proforma": self.env.context.get("proforma", False),
            "force_email": True,
            "model_description": "sale proposal",
        }
        self.state = "sent"
        # Return the action to open the email composition window
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }

    def get_proposal_url(self):
        self.ensure_one()
        return f'/my/proposal/{self.id}'

    def action_preview_sale_order(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "target": "self",
            "url": self.get_proposal_url(),
        }

    def action_confirm(self):
        # Create Sale Order
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner_id.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": line.product_id.id,
                            "product_uom_qty": line.product_uom_qty,
                            "price_unit": line.price_unit,
                        },
                    )
                    for line in self.order_line
                ],
            }
        )
        sale_order.action_confirm()
        self.sale_order_id = sale_order.id

    def action_accept(self):
        self.ensure_one()
        if self.state != "sent":
            raise UserError(_("Cannot accept a proposal that has not been sent."))

        self.state = "confirm"
        self.proposal_status = "approved"
        self.action_confirm()  # Confirm and create the sale order

    def action_reject(self):
        self.ensure_one()
        self.state = "cancel"
        self.proposal_status = "rejected"  # Ensure this field reflects the rejection status

    def write(self, vals):
        if 'proposal_status' in vals and vals['proposal_status'] in ['approved', 'rejected']:
            raise UserError(_("You cannot manually change the proposal status to approved or rejected."))
        return super().write(vals)


class SaleProposalLine(models.Model):
    _name = "sale.proposal.line"
    _description = "Sale Proposal Line"

    proposal_id = fields.Many2one(
        comodel_name="sale.proposal",
        string="Proposal Reference",
        required=True,
        ondelete="cascade",
        index=True,
        copy=False,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
    )
    product_uom_qty = fields.Float(
        string="Quantity", digits="Product Unit of Measure", required=True, default=1.0
    )
    price_unit = fields.Float(string="Unit Price", required=True, default=0.0)
    tax_id = fields.Many2many(
        comodel_name="account.tax",
        string="Taxes",
        domain=["|", ("active", "=", False), ("active", "=", True)],
    )
    price_subtotal = fields.Float(
        string="Subtotal", compute="_compute_price_subtotal", store=True
    )

    @api.depends("product_uom_qty", "price_unit", "tax_id")
    def _compute_price_subtotal(self):
        for line in self:
            price = line.price_unit * line.product_uom_qty
            line.price_subtotal = price


# Create a new record in the ir.sequence model for the sequence
class IrSequence(models.Model):
    _inherit = "ir.sequence"

    @api.model
    def _create_sequences(self):
        self.env['ir.sequence'].create({
            'name': 'Sale Proposal',
            'code': 'sale.proposal',
            'prefix': 'Proposal/%Y/%b/',
            'padding': 5,
            'number_increment': 1,
        })
