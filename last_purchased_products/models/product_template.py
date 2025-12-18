from dateutil.relativedelta import relativedelta
import datetime

from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_order = fields.Datetime(compute="_compute_last_order")
    last_invoice_date = fields.Datetime(compute="_compute_last_invoice_date")

    @api.depends_context("customer", "formatted_display_name")
    def _compute_display_name(self):
        res = super()._compute_display_name()
        if not self.env.context.get("customer") or not self.env.context.get(
            "formatted_display_name"
        ):
            return res

        compute_agotime_ref = self.compute_agotime
        for template in self:
            if not template.last_order:
                continue
            ago = compute_agotime_ref(template.last_order)
            current_product_template_name = template.display_name or ""
            if self.env.context.get("formatted_display_name"):
                if ago:
                    time_postfix = f"\t--{ago}--"
                else:
                    time_postfix = ""
                template.display_name = f"{current_product_template_name}{time_postfix}"
            else:
                template.display_name = f"{current_product_template_name}"

    @api.depends_context("customer")
    def _compute_last_order(self):
        last_orders = self.env["sale.order.line"].search(
            [
                ("order_id.partner_id", "=", self.env.context.get("customer")),
                ("product_id.product_tmpl_id", "in", self.ids),
                ("state", "=", "sale"),
            ],
            order="order_id desc",
        )
        order_dates = {}
        for order in last_orders:
            if order.product_id.id not in order_dates:
                order_dates[order.product_id.product_tmpl_id.id] = (
                    order.order_id.date_order
                )
        for template in self:
            template.last_order = order_dates.get(template.id, False)

    @api.depends_context("customer")
    def _compute_last_invoice_date(self):
        last_invoice_dates = self.env["account.move.line"].search(
            [
                ("partner_id", "=", self.env.context.get("customer")),
                ("product_id.product_tmpl_id", "in", self.ids),
                ("parent_state", "=", "posted"),
            ],
            order="create_date desc",
        )
        invoice_dates = {}
        for invoice in last_invoice_dates:
            if invoice.product_id.id not in invoice_dates:
                invoice_dates[invoice.product_id.product_tmpl_id.id] = invoice.create_date
        for template in self:
            template.last_invoice_date = invoice_dates.get(template.id, False)

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        customer_id = self.env.context.get("customer")
        if not customer_id:
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
