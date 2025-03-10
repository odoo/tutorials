from odoo import api, models
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _create_picking_from_pos_order_lines(self, location_dest_id, lines, picking_type, partner=False):
        pos_order = lines.mapped("order_id")
        # Ensure a shipping date is set before proceeding
        if not pos_order.select_shipping_date:
            return super()._create_picking_from_pos_order_lines(location_dest_id, lines, picking_type)
        # Check if an existing picking is already linked to this order and is not done
        existing_picking = self.search([
            ('pos_order_id', '=', pos_order.id),
            ('picking_type_id', '=', picking_type.id),
            ('state', '!=', 'done')
        ], limit=1)
        if existing_picking:
            try:
                with self.env.cr.savepoint():
                    existing_picking._action_done()
                return existing_picking
            except (UserError, ValidationError):
                pass
                return existing_picking
        #Check if stock moves already exist for this order
        existing_moves = self.env['stock.move'].search([
            ('origin', '=', pos_order.name),
            ('state', 'not in', ['done', 'cancel'])
        ])
        if existing_moves:
            raise UserError(f"Stock moves already exist for POS Order {pos_order.name}, skipping creation.")
        return super()._create_picking_from_pos_order_lines(location_dest_id, lines, picking_type)
