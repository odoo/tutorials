from dateutil.relativedelta import relativedelta
import datetime

from odoo import models, api, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    last_order = fields.Datetime(compute="_compute_last_order")
    last_invoice_date = fields.Datetime(compute="_compute_last_invoice_date")
    last_invoice_time = fields.Char(compute="_compute_invoice_time")

    @api.depends_context("customer", "formatted_display_name")
    def _compute_display_name(self):
        res = super()._compute_display_name()
        if not self.env.context.get("customer") or not self.env.context.get(
            "formatted_display_name"
        ):
            return res
        compute_agotime_ref = self.compute_agotime
        for product in self:
            if not product.last_order:
                continue
            ago = compute_agotime_ref(product.last_order)
            current_product_name = product.display_name or ""
            if self.env.context.get("formatted_display_name"):
                if ago:
                    time_postfix = f"\t--{ago}--"
                else:
                    time_postfix = ""
                product.display_name = f"{current_product_name}{time_postfix}"
            else:
                product.display_name = f"{current_product_name}"

    @api.depends_context("customer", "vendor")
    def _compute_last_invoice_date(self):
        customer_id = self.env.context.get("customer")
        vendor_id = self.env.context.get("vendor")
        domain = [
            ("product_id", "in", self.ids),
            ("parent_state", "=", "posted"),
        ]
        if customer_id:
            domain.append(("move_id.move_type", "=", "out_invoice"))
            domain.append(("partner_id", "=", customer_id))
        elif vendor_id:
            domain.append(("move_id.move_type", "=", "in_invoice"))
            domain.append(("partner_id", "=", vendor_id))
        else:
            pass

        last_invoice_dates = self.env["account.move.line"].search(
            domain, order="create_date desc"
        )
        invoice_dates = {}
        for invoice in last_invoice_dates:
            if invoice.product_id.id not in invoice_dates:
                invoice_dates[invoice.product_id.id] = invoice.create_date
        for product in self:
            product.last_invoice_date = invoice_dates.get(product.id, False)

    @api.depends_context("customer")
    def _compute_last_order(self):
        last_orders = self.env["sale.order.line"].search(
            [
                ("order_id.partner_id", "=", self.env.context.get("customer")),
                ("product_id", "in", self.ids),
                ("state", "=", "sale"),
            ],
            order="order_id desc",
        )
        order_dates = {}
        for order in last_orders:
            if order.product_id.id not in order_dates:
                order_dates[order.product_id.id] = order.order_id.date_order
        for product in self:
            product.last_order = order_dates.get(product.id, False)

    @api.depends('last_invoice_date')
    def _compute_invoice_time(self):
        compute_agotime_ref = self.compute_agotime
        for product in self:
            if product.last_invoice_date:
                ago = compute_agotime_ref(product.last_invoice_date)
                if not ago or ("s" in ago):
                    ago = "Just Now"
                product.last_invoice_time = ago
            else:
                product.last_invoice_time = False

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if not self.env.context.get("customer") and not self.env.context.get("vendor"):
            return super().name_search(name, args, operator, limit)
        res = super().name_search(name, args, operator, limit=100)
        ids = [r[0] for r in res]
        records = self.browse(ids)
        records.mapped("last_invoice_date")
        sorted_records = records.sorted(
            key=(lambda r: r.last_invoice_date or datetime.datetime.min), reverse=True
        )
        return [(r.id, r.display_name) for r in sorted_records][:limit]

    def compute_agotime(self, datetime_field):
        now = fields.Datetime.now()
        rd = relativedelta(now, datetime_field)
        if rd.years:
            ago = f"{rd.years}y"
        elif rd.months:
            ago = f"{rd.months}mo"
        elif rd.days:
            ago = f"{rd.days}d"
        elif rd.hours:
            ago = f"{rd.hours}h"
        elif rd.minutes:
            ago = f"{rd.minutes}m"
        elif rd.seconds:
            ago = f"{rd.seconds}s"
        else:
            ago = ""

        return ago
