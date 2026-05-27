from odoo import models, Command, api
from collections import defaultdict
from odoo.tools.float_utils import float_repr


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def write(self, values):
        super().write(values)
        if (
            self.order_id.discount_record_id
            and self.product_id != self.company_id.sale_discount_product_id
        ):
            trigger_fields = {"price_unit", "product_uom_qty", "tax_ids", "discount"}
            if not any(key in values for key in trigger_fields):
                return
            discount_product = self.company_id.sale_discount_product_id
            amount = self.order_id.discount_record_id.discount_percentage * 100.0
            order = self.order_id
            AccountTax = self.env["account.tax"]
            discount_lines = self.order_id.order_line.filtered_domain(
                [("product_id", "=", discount_product)]
            )
            order_lines = (
                order.order_line.filtered(lambda x: not x.display_type) - discount_lines
            )
            base_lines = [
                line._prepare_base_line_for_taxes_computation() for line in order_lines
            ]
            AccountTax._add_tax_details_in_base_lines(base_lines, order.company_id)
            AccountTax._round_base_lines_tax_details(base_lines, order.company_id)

            def grouping_function(base_line):
                return {"product_id": discount_product}

            global_discount_base_lines = AccountTax._prepare_global_discount_lines(
                base_lines=base_lines,
                company=self.company_id,
                amount_type="percent",
                amount=amount,
                computation_key=f"global_discount,{self.order_id.discount_record_id.discount_id}",
                grouping_function=grouping_function,
            )
            update_commands = [Command.unlink(line.id) for line in discount_lines]
            update_commands += [
                Command.create(values)
                for values in self._prepare_global_discount_so_lines(
                    global_discount_base_lines
                )
            ]
            self.order_id.with_context(is_global_discount_recompute=True).write(
                {
                    "discount_record_id": self.order_id.discount_record_id,
                    "order_line": update_commands,
                }
            )

    @api.ondelete(at_uninstall=False)
    def _unlink_sale_order_line(self):
        if self.env.context.get("is_global_discount_recompute"):
            return
        all_global_discount_lines = self.order_id.order_line.filtered_domain(
            [("product_id", "=", self.company_id.sale_discount_product_id)]
        )
        global_discount_lines_to_delete = self.filtered_domain(
            [("product_id", "=", self.company_id.sale_discount_product_id)]
        )
        if all_global_discount_lines == global_discount_lines_to_delete:
            self.order_id.write({"discount_record_id": False})
            return
        if global_discount_lines_to_delete == self:
            return
        self -= global_discount_lines_to_delete
        lines_grouped_by_tax_ids = self._group_lines_by_tax()
        for group in lines_grouped_by_tax_ids:
            self._recompute_specific_tax_discount(
                group, global_discount_lines_to_delete
            )

    def _recompute_specific_tax_discount(self, lines, global_discount_lines_to_delete):
        discount_product = self.company_id.sale_discount_product_id
        target_discount_line = self.order_id.order_line.filtered_domain(
            [("product_id", "=", discount_product), ("tax_ids", "=", lines.tax_ids)]
        )
        if target_discount_line in global_discount_lines_to_delete:
            return
        source_lines = self.order_id.order_line.filtered_domain(
            [
                ("product_id", "!=", discount_product),
                ("tax_ids", "=", target_discount_line.tax_ids),
            ]
        )
        if lines == source_lines:
            target_discount_line.unlink()
            return
        discount_percentage = self.order_id.discount_record_id.discount_percentage * 100
        source_lines -= lines
        base_lines = [
            line._prepare_base_line_for_taxes_computation() for line in source_lines
        ]
        AccountTax = self.env["account.tax"]
        AccountTax._add_tax_details_in_base_lines(base_lines, self.company_id)
        AccountTax._round_base_lines_tax_details(base_lines, self.company_id)
        new_data = self.env["account.tax"]._prepare_global_discount_lines(
            base_lines=base_lines,
            company=self.company_id,
            amount_type="percent",
            amount=discount_percentage,
            computation_key=f"global_discount,{self.order_id.discount_record_id.discount_id}",
            grouping_function=lambda l: {"product_id": discount_product},
        )
        target_discount_line.write(
            self._prepare_global_discount_so_lines(new_data, target_discount_line.name)[
                0
            ]
        )

    def _prepare_global_discount_so_lines(self, base_lines, name=None):
        AccountTax = self.env["account.tax"]
        so_line_values_list = []
        for base_line in base_lines:
            if not name:
                AccountTax = self.env["account.tax"]
                discount_dp = self.env["decimal.precision"].precision_get("Discount")
                has_multiple_tax_combinations = (
                    len(
                        {
                            base_line["tax_ids"]
                            for base_line in base_lines
                            if base_line["tax_ids"]
                        }
                    )
                    > 1
                )
                if has_multiple_tax_combinations:
                    name = self.env._(
                        "Discount %(percent)s%%"
                        "- On products with the following taxes %(taxes)s",
                        percent=float_repr(
                            self.order_id.discount_record_id.discount_percentage
                            * 100.0,
                            discount_dp,
                        ),
                        taxes=", ".join(base_line["tax_ids"].mapped("name")),
                    )
                else:
                    name = self.env._(
                        "Discount %(percent)s%%",
                        percent=float_repr(
                            self.order_id.discount_record_id.discount_percentage
                            * 100.0,
                            discount_dp,
                        ),
                    )
            so_line_values_list.append(
                {
                    "name": name,
                    "product_id": base_line["product_id"].id,
                    "price_unit": base_line["price_unit"],
                    "technical_price_unit": 0,
                    "product_uom_qty": base_line["quantity"],
                    "tax_ids": [Command.set(base_line["tax_ids"].ids)],
                    "extra_tax_data": AccountTax._export_base_line_extra_tax_data(
                        base_line
                    ),
                    "sequence": 999,
                }
            )
        return so_line_values_list

    def _group_lines_by_tax(self):
        grouped_map = defaultdict(lambda: self.env["sale.order.line"])
        for line in self:
            tax_key = tuple(sorted(line.tax_ids.ids))
            grouped_map[tax_key] |= line
        return list(grouped_map.values())
