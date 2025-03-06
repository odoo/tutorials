# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = "Sales Order Lines"

    distributed_price = fields.Float(string="Distributed Price")
    distributed_price_tags = fields.Many2many(
        "sale.order.distribution.tag",
        string="Division",
        compute="_compute_distributed_price_tags",
        store=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super(SaleOrderLine, self).create(vals_list)
        for record in records:
            record._compute_distributed_price_tags()
        return records

    @api.depends("distributed_price")
    def _compute_distributed_price_tags(self):
        for line in self:
            tags = []
            rounded_price = round(line.distributed_price, 2)
            latest_distribution = self.env["sale.order.line.distribution"].search(
                [("target_sale_order_line_id", "=", line.id)],
                order="id desc",
                limit=1,
            )

            new_tag = self.env["sale.order.distribution.tag"].create(
                {
                    "name": str(rounded_price),
                    "color": 2
                    if line.distributed_price == 0
                    else latest_distribution.source_sale_order_line_id % 10,
                }
            )
            tags.append(new_tag.id)

            line.distributed_price_tags = [(6, 0, tags)]
    
    def unlink(self):
        for record in self:
            self_distributions = record.env["sale.order.line.distribution"].search(
                [("source_sale_order_line_id", "=", record.id)]
            )

            distributions = self.env['sale.order.line.distribution'].search([
                ('target_sale_order_line_id', '=', record.id)
            ])

            for dist in self_distributions:
                if dist.price > 0:
                    destination_line = record.env["sale.order.line"].browse(dist.target_sale_order_line_id)
                    if destination_line:
                        destination_line.distributed_price -= dist.price
                        destination_line.price_subtotal -= dist.price
                    dist.unlink()

            for dist in distributions:
                source_sale_order_line = self.env['sale.order.line'].browse(dist.source_sale_order_line_id)
                if source_sale_order_line.exists():
                    source_sale_order_line.write({
                        # 'distributed_price': source_sale_order_line.distributed_price + dist.price,
                        'price_subtotal': source_sale_order_line.price_subtotal + dist.price
                    })
                dist.unlink()
        return super().unlink()

    def open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Distributed Price',
            'res_model': 'sale.order.line.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id' : self.id,
            }
        }

class SaleOrderLineDistribution(models.Model):
    _name = "sale.order.line.distribution"
    _description = "Tracks Distributed Prices Between Sale Order Lines"

    source_sale_order_line_id = fields.Integer(string="Source Sale Order Line")
    target_sale_order_line_id = fields.Integer(string="Target Sale Order Line")
    price = fields.Float(string="Distributed Price", required=True)

class SaleOrderDistributionTag(models.Model):
    _name = "sale.order.distribution.tag"
    _description = "Sale Order Distribution Tags"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color", default=3)
