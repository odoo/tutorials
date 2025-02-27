from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    distributed_price = fields.Float(string="Division", store=True)
    unit_price = fields.Float(string="Unit Price", compute="_compute_unit_price")
    source_order_line_ids = fields.One2many(
        "sale.order.line.distribution", "source_order_line_id"
    )

    @api.depends("price_subtotal", "product_uom_qty")
    def _compute_unit_price(self):
        for line in self:
            line.unit_price = line.price_subtotal / line.product_uom_qty

    def get_total_distributed_price_of_line(self, line):
        for record in self:
            total_distributed_price = 0
            for temp_line in record.order_id.order_line:
                if line.id == temp_line.id:
                    total_distributed_price = sum(
                        self.env["sale.order.line.distribution"]
                        .search(
                            [
                                ("destination_order_line_id", "=", temp_line.id),
                            ]
                        )
                        .mapped("price")
                    )

            return total_distributed_price

    def unlink(self):
        for record in self:
            current_line_as_source = record.source_order_line_ids

            for line in record.order_id.order_line:
                if line.id != record.id:
                    temp_line = self.env["sale.order.line.distribution"].search(
                        [
                            ("source_order_line_id", "=", line.id),
                            ("destination_order_line_id", "=", record.id),
                        ]
                    )
                    total_distributed_price = (
                        record.get_total_distributed_price_of_line(line)
                    )
                    value_to_add_in_distribution = (
                        total_distributed_price - line.distributed_price
                    )
                    line.distributed_price += (
                        value_to_add_in_distribution
                        if value_to_add_in_distribution <= temp_line.price
                        else temp_line.price
                    )
                    line.price_subtotal += temp_line.price
                    temp_line.unlink()

            for line in current_line_as_source:
                destination_line = line.destination_order_line_id
                destination_line.distributed_price -= line.price
                destination_line.price_subtotal -= line.price
                line.unlink()
            record.source_order_line_ids.unlink()

        return super().unlink()
