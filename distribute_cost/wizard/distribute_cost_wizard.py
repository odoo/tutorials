from odoo import fields,models,api

class DistributeCostWizard(models.TransientModel):
    _name = "distribute.cost.wizard"
    _description = "Distribute cost Wizard"

    order_id = fields.Many2one(
        "sale.order",
        default=lambda self: self.env["sale.order.line"]
        .browse(self._context["active_id"])
        .order_id,
    )
    order_line_ids = fields.Many2many(
        "sale.order.line", compute="_compute_order_lines", readonly=False
    )

    @api.depends("order_id")
    def _compute_order_lines(self):
        print("======================",self.read(),"======================")
        for record in self:
            if record.order_id:
                record.order_line_ids = record.order_id.order_line.ids
                record.order_line_ids = record.order_id.order_line.filtered(
                    lambda line: line
                    != self.env["sale.order.line"].browse(self._context["active_id"])
                )
            else:
                record.order_line_ids = []
            print("==============================Order Line Ids========================",record.order_line_ids)

    def action_divide_cost(self):
        print("============Divide Action Called========")
        pass