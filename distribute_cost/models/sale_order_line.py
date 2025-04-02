from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    division_price = fields.Float(string="Division Price", store=True)  # received amount from distributed order line
    distributed_line = fields.Many2one('sale.order.line', store=True)  # reffer distributed line
    divided_cost_tags = fields.Many2many('divided.cost.tag', string='division' , compute='_compute_divided_cost_tags', store=True)  # division tag

    @api.depends('division_price', 'distributed_line')
    def _compute_divided_cost_tags(self):

        for line in self:
            tags = []
            if line.distributed_line and line.division_price > 0:
                if line.id == line.distributed_line.id:
                    rounded_price = round(line.division_price, 2)
                    tag = self.env['divided.cost.tag'].create({
                        'name': f"{rounded_price}",
                        'color': 1,
                    })
                    tags.append(tag.id)
                    line.divided_cost_tags = [(6, 0, tags)]
                else:
                    tag = self.env['divided.cost.tag'].create({
                        'name': f"{line.division_price}",
                        'color': 5,
                    })
                    tags.append(tag.id)
                    line.divided_cost_tags = [(6, 0, tags)]

    #  handle order line delete case:
    def unlink(self):
        for line in self:
            # if deleted line is itself distributed line
            if line.id == line.distributed_line.id:
                # fatch all order line which received amount from this distributed order line
                added_order_lines = line.order_id.order_line.filtered(
                    lambda l: l.distributed_line.id == line.id
                )
                # substract distributed amount in receiver order line
                for line in added_order_lines:
                    line.price_subtotal -= line.division_price
                    line.division_price = 0.0
                    line.distributed_line = None
                    line.divided_cost_tags.unlink()
                    line.divided_cost_tags = None

            # else if deleted line is receiver : add received amount back to the distributed oeder line
            elif line.distributed_line:
                line.distributed_line.price_subtotal += line.division_price
                line.distributed_line.division_price += line.division_price
                line.price_subtotal -= line.division_price
                line.division_price = 0.0
                line.distributed_line = None
                line.divided_cost_tags.unlink()
                line.divided_cost_tags = None
        return super().unlink()
