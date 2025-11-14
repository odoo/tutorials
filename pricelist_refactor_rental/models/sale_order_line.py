from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_pricelist_price(self):
        """ Compute the price given by the pricelist for the given line information.

        :return: the product sales price in the order currency (without taxes)
        :rtype: float
        """
        if self.product_template_id.rent_ok:
            self.ensure_one()
            self.product_id.ensure_one()
            self.order_id._rental_set_dates()

            return self.order_id.pricelist_id._get_product_price(
                product=self.product_id.with_context(**self._get_product_price_context()),
                quantity=self.product_uom_qty or 1.0,
                currency=self.currency_id,
                uom=self.product_uom,
                date=self.order_id.date_order or fields.Date.today(),
                start_date=self.start_date,
                end_date=self.return_date,
            )
        return super()._get_pricelist_price()

    @api.depends('order_id.rental_start_date', 'order_id.rental_return_date')
    def _compute_pricelist_item_id(self):
        """ Computes the pricelist item applicable to the given line.

        In the rental case, the applicable pricelist item is the one that matches the
        product, the quantity, the uom, the date, and the duration of the rental.
        """
        if self.order_id.rental_start_date and self.order_id.rental_return_date:
            for line in self:
                if not line.product_id or line.display_type or not line.order_id.pricelist_id:
                    line.pricelist_item_id = False
                else:
                    line.pricelist_item_id = line.order_id.pricelist_id._get_product_rule(
                        product=line.product_id,
                        quantity=line.product_uom_qty or 1.0,
                        uom=line.product_uom,
                        date=line.order_id.date_order,
                        start_date=line.start_date,
                        end_date=line.return_date,
                    )
        else:
            super()._compute_pricelist_item_id()

    def _get_pricelist_price_before_discount(self):
        """ Compute the price used as base for the pricelist price computation.

        :return: the product sales price in the order currency (without taxes)
        :rtype: float
        """
        if self.start_date and self.return_date:
            self.ensure_one()
            self.product_id.ensure_one()

            return self.pricelist_item_id._compute_price_before_discount(
                product=self.product_id.with_context(**self._get_product_price_context()),
                quantity=self.product_uom_qty or 1.0,
                uom=self.product_uom,
                date=self.order_id.date_order,
                currency=self.currency_id,
                start_date=self.start_date,
                end_date=self.return_date,
            )
        return super()._get_pricelist_price_before_discount()
