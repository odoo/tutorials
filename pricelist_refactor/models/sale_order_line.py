from odoo import api, Command, fields, models
from collections import defaultdict


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_pricelist_price(self):
        """Compute the price given by the pricelist for the given line information.

        :return: the product sales price in the order currency (without taxes)
        :rtype: float
        """
        self.ensure_one()
        self.product_id.ensure_one()
        if self.product_template_id.rent_ok:
            self.order_id._rental_set_dates()
            return self.order_id.pricelist_id._get_product_price(
                self.product_id.with_context(**self._get_product_price_context()),
                self.product_uom_qty or 1.0,
                currency=self.currency_id,
                uom=self.product_uom,
                date=self.order_id.date_order or fields.Date.today(),
                start_date=self.start_date,
                end_date=self.return_date,
            )
        elif self.product_template_id.recurring_invoice:
            if self.order_id.plan_id and self.order_id.pricelist_id:
                pricelist_item_id = self.env['product.pricelist.item']._get_first_suitable_recurring_pricing(
                    self.product_id, self.order_id.plan_id, self.pricelist_id
                )
            else:
                pricelist_item_id = self.pricelist_item_id
            return pricelist_item_id._compute_price(
                self.product_id.with_context(**self._get_product_price_context()),
                self.product_uom_qty or 1.0,
                self.product_uom,
                self.order_id.date_order,
                self.currency_id,
                self.order_id.plan_id
            )
        return self.pricelist_item_id._compute_price(
            self.product_id.with_context(**self._get_product_price_context()),
            self.product_uom_qty or 1.0,
            self.product_uom,
            self.order_id.date_order,
            self.currency_id,
        )

    @api.depends('order_id.subscription_state', 'order_id.start_date', 'order_id.rental_start_date', 'order_id.rental_return_date')
    def _compute_discount(self):
        """ For upsells : this method compute the prorata ratio for upselling when the current and possibly future
                        period have already been invoiced.
                        The algorithm work backward by trying to remove one period at a time from the end to have a number of
                        complete period before computing the prorata for the current period.
                        For the current period, we use the remaining number of days / by the number of day in the current period.
        """
        today = fields.Date.today()
        other_lines = self.env['sale.order.line']
        line_per_so = defaultdict(lambda: self.env['sale.order.line'])
        for line in self:
            if not line.recurring_invoice:
                other_lines += line  # normal sale line are handled by super
            else:
                line_per_so[line.order_id._origin.id] += line

        for so_id, lines in line_per_so.items():
            order_id = self.env['sale.order'].browse(so_id)
            parent_id = order_id.subscription_id
            if not parent_id:
                other_lines += lines
                continue
            if not parent_id.next_invoice_date or order_id.subscription_state != '7_upsell':
                # We don't apply discount
                continue
            start_date = max(order_id.start_date or today, order_id.first_contract_date or today)
            end_date = parent_id.next_invoice_date
            if start_date >= end_date:
                ratio = 0
            else:
                recurrence = parent_id.plan_id.billing_period
                complete_rec = 0
                while end_date - recurrence >= start_date:
                    complete_rec += 1
                    end_date -= recurrence
                ratio = (end_date - start_date).days / ((start_date + recurrence) - start_date).days + complete_rec
            # If the parent line had a discount, we reapply it to keep the same conditions.
            # E.G. base price is 200€, parent line has a 10% discount and upsell has a 25% discount.
            # We want to apply a final price equal to 200 * 0.75 (prorata) * 0.9 (discount) = 135 or 200*0,675
            # We need 32.5 in the discount
            add_comment = False
            line_to_discount, discount_comment = lines._get_renew_discount_info()
            for line in line_to_discount:
                if line.parent_line_id and line.parent_line_id.discount:
                    line.discount = (1 - ratio * (1 - line.parent_line_id.discount / 100)) * 100
                else:
                    line.discount = (1 - ratio) * 100
                # Add prorata reason for discount if necessary
                if ratio != 1 and "(*)" not in line.name:
                    line.name += "(*)"
                    add_comment = True
            if add_comment and not any((l.display_type == 'line_note' and '(*)' in l.name) for l in order_id.order_line):
                order_id.order_line = [Command.create({
                    'display_type': 'line_note',
                    'sequence': 999,
                    'name': discount_comment,
                    'product_uom_qty': 0,
                })]
        discount_enabled = self.env['product.pricelist.item']._is_discount_feature_enabled()
        for line in other_lines:
            if not line.product_id or line.display_type:
                line.discount = 0.0

            if not (line.order_id.pricelist_id and discount_enabled):
                continue

            line.discount = 0.0
            if not (line.pricelist_item_id and line.pricelist_item_id._show_discount()):
                # No pricelist rule was found for the product
                # therefore, the pricelist didn't apply any discount/change
                # to the existing sales price.
                continue
            line = line.with_company(line.company_id)
            pricelist_price = line._get_pricelist_price()
            base_price = line._get_pricelist_price_before_discount()
            if base_price != 0:  # Avoid division by zero
                discount = (base_price - pricelist_price) / base_price * 100
                if (discount > 0 and base_price > 0) or (discount < 0 and base_price < 0):
                    # only show negative discounts if price is negative
                    # otherwise it's a surcharge which shouldn't be shown to the customer
                    line.discount = discount

    def _compute_pricelist_item_id(self):
        for line in self:
            if not line.product_id or line.display_type or not line.order_id.pricelist_id:
                line.pricelist_item_id = False
            else:
                line.pricelist_item_id = line.order_id.pricelist_id._get_product_rule(
                    line.product_id,
                    quantity=line.product_uom_qty or 1.0,
                    uom=line.product_uom,
                    date=line.order_id.date_order,
                    plan_id=line.order_id.plan_id,
                    start_date=line.start_date,
                    end_date=line.return_date,
                )

    def _get_pricelist_price_before_discount(self):
        """Compute the price used as base for the pricelist price computation.

        :return: the product sales price in the order currency (without taxes)
        :rtype: float
        """
        self.ensure_one()
        self.product_id.ensure_one()
        converted_duration = None
        recurrence_id = None
        plan_id = None
        if self.start_date and self.return_date:
            duration_vals = self.pricelist_item_id._compute_duration_vals(self.start_date, self.return_date)
            duration = self.pricelist_item_id and duration_vals[self.pricelist_item_id.recurrence_id.unit or 'day'] or 0
            converted_duration = duration
            recurrence_id=self.pricelist_item_id.recurrence_id
        elif self.order_id.plan_id:
            plan_id = self.order_id.plan_id
        return self.pricelist_item_id._compute_price_before_discount(
            product=self.product_id.with_context(**self._get_product_price_context()),
            quantity=self.product_uom_qty or 1.0,
            uom=self.product_uom,
            date=self.order_id.date_order,
            currency=self.currency_id,
            plan_id=plan_id,
            converted_duration=converted_duration,
            recurrence_id=recurrence_id
        )
        return super()._get_pricelist_price_before_discount()
