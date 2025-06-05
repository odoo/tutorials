from odoo import models, fields, api, Command
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round

class ReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    sale_order_id = fields.Many2one(
        'sale.order',
        string="Sale Order",
    )
    purchase_order_id = fields.Many2one(
        'purchase.order', 
        string="Purchase Order",
    )   

    @api.onchange("product_id")
    def _onchange_product_id_and_picking_id(self):
        self.sale_order_id = None
        self.purchase_order_id = None

class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    picking_ids = fields.Many2many(
        'stock.picking', 
        string="Pickings", 
    )

    @api.model
    def default_get(self, fields_list):
        orig_active_ids = self.env.context.get('active_ids', [])
        pickings = self.env['stock.picking'].browse(orig_active_ids)
        ctx = dict(self.env.context)
        if orig_active_ids and len(orig_active_ids) > 1:
            ctx['active_ids'] = [orig_active_ids[0]]
        res = super(ReturnPicking, self.with_context(ctx)).default_get(fields_list)
        res['picking_ids'] = orig_active_ids
        return res

    @api.depends('picking_ids')
    def _compute_moves_locations(self):    
        for wizard in self:
            if len(wizard.picking_ids) == 1:
                super()._compute_moves_locations()
            else:
                wizard.product_return_moves = []

    def _assign_move_ids(self):
        is_delivery = self.env.context.get('is_delivery')
        for return_move in self.product_return_moves:
            if not return_move.move_id:
                if is_delivery:
                    linked_move = self.picking_ids.move_ids.filtered(
                        lambda m: m.product_id == return_move.product_id and
                                  m.picking_id.sale_id == return_move.sale_order_id
                    )
                else:
                    linked_move = self.picking_ids.move_ids.filtered(
                        lambda m: m.product_id == return_move.product_id and
                                  m.picking_id.purchase_id == return_move.purchase_order_id
                    )
                if linked_move:
                    return_move.move_id = linked_move.id

    def _create_return(self):
        is_delivery = self.env.context.get('is_delivery')
        self._assign_move_ids()
        new_picking = super()._create_return()
        if is_delivery:
            new_picking['new_return_ids'] = self.picking_ids.filtered(
                lambda p: p.sale_id in self.product_return_moves.mapped('sale_order_id')
            )
            new_picking['sale_ids'] = self.product_return_moves.mapped('sale_order_id')
            new_picking['origin'] = ', '.join(self.product_return_moves.mapped('sale_order_id.name'))
        else:
            new_picking['new_return_ids'] = self.picking_ids.filtered(
                lambda p: p.purchase_id in self.product_return_moves.mapped('purchase_order_id')
            )
            new_picking['purchase_ids'] = self.product_return_moves.mapped('purchase_order_id')
            new_picking['origin'] = ', '.join(self.product_return_moves.mapped('purchase_order_id.name'))
        return new_picking
    
    def action_create_exchanges(self):
        self.ensure_one()
        if len(self.picking_ids) == 1:
            return super().action_create_exchanges()
        action = self.action_create_returns()
        proc_list = []
        origin = ', '.join(self.product_return_moves.mapped('sale_order_id.name'))
        for line in self.product_return_moves:
            if not line.move_id:
                continue
            proc_values = self._get_proc_values(line)
            proc_list.append(self.env["procurement.group"].Procurement(
                line.product_id, line.quantity, line.uom_id,
                line.move_id.location_dest_id or self.picking_id.location_dest_id,
                line.product_id.display_name,
                origin, 
                self.picking_id.company_id,
                proc_values,
            ))
        if proc_list:
            self.env['procurement.group'].run(proc_list)
            is_delivery = self.env.context.get('is_delivery')
            if is_delivery:
                sale_orders = self.product_return_moves.mapped('sale_order_id')
                if sale_orders:
                    new_picking = self.env["stock.picking"].search([
                            ("state", "=", "assigned"),
                            ("origin", "=", origin),
                        ],
                        order="id desc",
                        limit=1,
                    )
                    if new_picking and sale_orders:
                        new_picking.write({
                            'sale_ids': [Command.link(order_id) for order_id in sale_orders.ids]
                        })
        return action
        
    def action_create_returns_all(self):
        self._assign_move_ids()
        return super().action_create_returns_all()
    
    def action_mass_return(self):
        wizard_title = ""
        pickings = self.env['stock.picking'].browse(self.env.context.get('active_ids', []))
        available_products = pickings.mapped('move_ids.product_id').ids
        invalid_pickings = pickings.filtered(lambda p: not p._can_return())
        error_message = ["The selected transfers can not be mass retuened. Please chech their status and operation types.",]
        is_delivery = True
        multi_pickings = False if len(pickings) == 1 else True

        if pickings:
            if invalid_pickings:
                error_message.append("\nIncompatibility: Status\n" + ", ".join([p.name for p in invalid_pickings]) + "\n")
            if all(picking.picking_type_id.code == 'outgoing' for picking in pickings):
                wizard_title = "Mass Return (Deliveries)"
            elif all(picking.picking_type_id.code == 'incoming' for picking in pickings):
                wizard_title = "Mass Return (Receipts)"
                is_delivery = False
            else:
                error = "\nIncompatibility: Operation Types\n"
                for picking in pickings:
                    error+="%s: %s\n" % (picking.name, picking.picking_type_id.code)
                error_message.append(error)
            if len(error_message)>1:
                raise UserError("\n".join(error_message))

        return {
            'name': wizard_title,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.return.picking',
            'target': 'new',
            'view_id': self.env.ref('mass_return.stock_return_picking_view_form').id,
            'context':dict(
                self.env.context, is_delivery=is_delivery, 
                available_products=available_products, 
                multi_pickings=multi_pickings,
                sale_orders=pickings.mapped('sale_id').ids,
                purchase_orders=pickings.mapped('purchase_id').ids,
                ),
        }
