# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models, Command
from odoo.exceptions import UserError


class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    picking_ids = fields.Many2many("stock.picking", string="Pickings")
    picking_type_id = fields.Many2one("stock.picking.type", string="Operation Type")
    allowed_product_ids = fields.Many2many(
        "product.product", string="Allowed Products"
    )

    @api.model
    def default_get(self, fields):
        active_ids = self.get_active_ids()
        if len(active_ids) == 1:
            return super().default_get(fields)
        res = {}
        pickings = self.env["stock.picking"].browse(active_ids)
        if any(p.state != "done" for p in pickings):
            raise UserError(_("All selected pickings must be in 'Done' state."))

        picking_type = pickings[0].picking_type_id
        if any(p.picking_type_id != picking_type for p in pickings):
            raise UserError(
                _("All selected pickings must have the same operation type.")
            )
        if picking_type.code == "outgoing":
            if any(not p.sale_id for p in pickings):
                raise UserError(_("All selected pickings must have a sale order."))
        else:
            for picking in pickings:
                purchase_order = self.env["purchase.order"].search(
                    [("picking_ids", "in", picking.ids)], limit=1
                )
                if not purchase_order:
                    raise UserError(
                        _("All selected pickings must have a purchase order.")
                    )

        res = {
            "picking_ids": [Command.set(active_ids)],
            "picking_id": pickings[0].id,
            "picking_type_id": picking_type.id,
            "allowed_product_ids": [Command.set(pickings.mapped("move_ids.product_id").ids)],
            "product_return_moves": [Command.clear()],
        }

        return res

    def get_active_ids(self):
        active_ids = self.env.context.get("active_ids", [])
        if isinstance(active_ids, int):
            active_ids = [active_ids]
        return active_ids

    def _get_picking_ids(self):
        return self.product_return_moves.filtered(
            lambda line: line.quantity > 0
        ).mapped("picking_id")

    def _get_origin(self):
        new_origin = "Return of "
        for picking in self._get_picking_ids():
            new_origin += picking.origin + ", "
        return new_origin[:-2]

    def create_picking_wizard(self, picking_id):
        return self.env["stock.return.picking"].create(
            {
                "picking_id": picking_id.id,
                "product_return_moves": [
                    Command.create(
                        {
                            "product_id": line.product_id.id,
                            "quantity": line.quantity,
                            "to_refund": line.to_refund,
                            "move_id": line.move_id.id,
                        },
                    )
                    for line in self.product_return_moves.filtered(
                        lambda l: l.picking_id == picking_id
                    )
                ],
            }
        )

    # Override _create_return
    def _create_return(self):
        for return_move in self.product_return_moves.move_id:
            return_move.move_dest_ids.filtered(lambda m: m.state not in ('done', 'cancel'))._do_unreserve()

        # create new picking for returned products
        new_picking = self.picking_id.copy(self._prepare_picking_default_values())
        new_picking.user_id = False
        new_picking.message_post_with_source(
            "mail.message_origin_link",
            render_values={"self": new_picking, "origin": self._get_picking_ids()},
            subtype_xmlid="mail.mt_note",
        )
        returned_lines = False
        for return_line in self.product_return_moves:
            if return_line._process_line(new_picking):
                returned_lines = True
        if not returned_lines:
            raise UserError(_("Please specify at least one non-zero quantity."))

        new_picking.action_confirm()
        new_picking.action_assign()
        return new_picking

    def action_create_returns_all(self):
        if len(self.get_active_ids()) == 1:
            return super().action_create_returns_all()
        new_picking = self._create_return()

        for picking in self._get_picking_ids():
            picking.write({"new_return_ids": [Command.link(new_picking.id)]})

        vals = {
            "sale_id": self._get_picking_ids()[0].sale_id.id,
            "sale_ids": self._get_picking_ids().mapped("sale_id").ids,
            "origin": self._get_origin(),
            "return_id": self._get_picking_ids()[0].id
        }

        new_picking.write(vals)
        return {
            "name": _("Returned Picking"),
            "view_mode": "form",
            "res_model": "stock.picking",
            "res_id": new_picking.id,
            "type": "ir.actions.act_window",
            "context": self.env.context,
        }

    def action_create_returns(self):
        new_pickings = None
        active_ids = self.get_active_ids()
        if len(active_ids) == 1:
            return super().action_create_returns()

        for picking_id in self._get_picking_ids():
            picking_return_wizard = self.create_picking_wizard(picking_id)

            new_pickings =picking_return_wizard.with_context(
                    active_ids=picking_id.id
                )._create_return()
            new_pickings.sale_id = picking_id.sale_id.id
            new_pickings.return_id = picking_id.id
            
        return {
            "name": _("Returned Pickings"),
            "view_mode": "form",
            "res_model": "stock.picking",
            "res_id": new_pickings.id,
            "type": "ir.actions.act_window",
            "context": self.env.context,
            }

    def create_exchanges(self):
        active_ids = self.get_active_ids()
        if len(active_ids) == 1:
            return super().action_create_exchanges()
        else:
            action = None
            for picking_id in self.picking_ids:
                picking_return_wizard = self.create_picking_wizard(picking_id)
                action = picking_return_wizard.with_context(
                    active_ids=picking_id.id
                ).action_create_exchanges()
        return action
