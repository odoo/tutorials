from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PriceDistributionWizard(models.TransientModel):
    _name = "price.distribution.wizard"

    order_id = fields.Many2one("sale.order")
    line_ids = fields.One2many(
        "price.distribution.line.wizard",
        inverse_name="wizard_id",
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_line_id = self._context.get("active_id")
        active_line = self.env["sale.order.line"].browse(active_line_id)
        order = active_line.order_id
        lines_to_divide = order.order_line.filtered(
            lambda line: line.id != active_line.id
        )
        lines = []
        for line in lines_to_divide:
            wizard_line = self.env["price.distribution.line.wizard"].create(
                {
                    "wizard_id": self.id,
                    "product": line.product_id.name,
                    "order_line_id": line.id,
                    "distributed_price": active_line.price_subtotal
                    / len(lines_to_divide)
                    if lines_to_divide
                    else 0,
                }
            )

            lines.append(wizard_line.id)
            res["line_ids"] = [(6, 0, lines)]
        return res

    def action_confirm_distribution(self):
        active_line = self.env["sale.order.line"].browse(self._context["active_id"])
        total_distributed_price = sum(
            self.line_ids.filtered(lambda line: line.include_for_division).mapped(
                "distributed_price"
            )
        )
        if total_distributed_price > active_line.price_subtotal:
            raise ValidationError("Distributed price must not exceed product amount")
        for line in self.line_ids:
            if line.include_for_division:
                existed_distribution = (
                    line.order_line_id.source_order_line_ids.filtered(
                        lambda dist: dist.source_order_line_id.id == active_line.id and dist.destination_order_line_id == line.order_line_id
                    )
                )
                if existed_distribution:
                    line.order_line_id.distributed_price -= existed_distribution.price
                    line.order_line_id.price_subtotal -= existed_distribution.price
                    existed_distribution.unlink()  # To delete existing distribution line
                line.order_line_id.distributed_price += line.distributed_price
                line.order_line_id.price_subtotal += line.distributed_price
                new_distribution = self.env["sale.order.line.distribution"].create({
                        "source_order_line_id": active_line.id,
                        "destination_order_line_id": line.order_line_id.id,
                        "price": line.distributed_price,
                    })
                active_line.write({
                        "source_order_line_ids": [(4, new_distribution.id)],
                    })
        active_line.price_subtotal -= total_distributed_price

        if active_line.distributed_price > 0:
            if active_line.price_subtotal == 0:
                active_line.distributed_price = 0
            elif total_distributed_price > (active_line.product_uom_qty * active_line.price_unit):
                active_line.distributed_price = active_line.distributed_price - (
                    total_distributed_price
                    - (active_line.product_uom_qty * active_line.price_unit)
                )


class PriceDistributionLineWizard(models.TransientModel):
    _name = "price.distribution.line.wizard"

    wizard_id = fields.Many2one("price.distribution.wizard", ondelete="cascade")
    product = fields.Char(readonly=True)
    order_line_id = fields.Many2one("sale.order.line")
    distributed_price = fields.Float()
    include_for_division = fields.Boolean(default=True)

    @api.onchange("include_for_division")
    def _onchange_include_for_division(self):
        if self.wizard_id:
            active_line_id = self._context.get("active_id")
            lines_to_divide = self.wizard_id.line_ids.filtered(
                lambda line: line.include_for_division
            )
            if lines_to_divide:
                total_price = (
                    self.env["sale.order.line"].browse(active_line_id).price_subtotal
                )
                for line in lines_to_divide:
                    line.distributed_price = total_price / len(lines_to_divide)

            if lines_to_divide:
                total_price = (
                    self.env["sale.order.line"].browse(active_line_id).price_subtotal
                )
                for line in lines_to_divide:
                    line.distributed_price = total_price / len(lines_to_divide)
