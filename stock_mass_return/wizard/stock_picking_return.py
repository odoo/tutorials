from odoo import api, Command, fields, models, _
from odoo.exceptions import UserError

class ReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
        domain="[('id', 'in', allowed_product_ids)]",
    )
    allowed_product_ids = fields.Many2many(
        "product.product",
        string="Allowed Products",
        related="wizard_id.allowed_product_ids",
        store=False,
    )
    allowed_picking_ids = fields.Many2many("stock.picking")
    picking_id = fields.Many2one(
        "stock.picking",
        domain="[('id', 'in', allowed_picking_ids)]",
    )
    allowed_sale_order_ids = fields.Many2many("sale.order")
    sale_order_id = fields.Many2one("sale.order", string="Sale Order", domain="[('id', 'in', allowed_sale_order_ids)]")
    allowed_purchase_order_ids = fields.Many2many("purchase.order")
    purchase_order_id = fields.Many2one("purchase.order", string="Purchase Order", domain="[('id', 'in', allowed_purchase_order_ids)]")
        
    def _prepare_move_default_values(self, new_picking):
        vals = super()._prepare_move_default_values(new_picking)
        vals["group_id"] = self.picking_id.group_id.id
        return vals

    @api.onchange("purchase_order_id")
    def _onchange_purchase_order_id(self):
        if self.purchase_order_id:
            self.picking_id = self.env["stock.picking"].search(
                [("id", "in", self.purchase_order_id.picking_ids.ids)], limit=1
            )

    @api.onchange("sale_order_id")
    def _onchange_sale_order_id(self):
        if self.sale_order_id:
            self.picking_id = self.wizard_id.picking_ids.filtered(
                lambda p: p.sale_id == self.sale_order_id._origin
            )

    @api.onchange("picking_id")
    def _onchange_picking_id(self):
        if self.product_id and self.picking_id:
            move = self.picking_id.move_ids.filtered(lambda m: m.product_id == self.product_id)
            self.move_id = move.id

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:

            self.allowed_picking_ids = self.wizard_id.picking_ids.filtered(
                lambda p: p.move_ids.filtered(
                    lambda m: m.product_id == self.product_id
                )
            ).ids

            if self.wizard_id.picking_type_id.code == "outgoing":
                allowed_sales = [
                    picking.sale_id.id
                    for picking in self.allowed_picking_ids
                    if picking.sale_id
                ]
                self.allowed_sale_order_ids = [(6, 0, allowed_sales)]
                self.sale_order_id = False
            else:
                allowed_purchase = self.env["purchase.order"].search([
                        ("picking_ids", "in", self.allowed_picking_ids.ids),
                        ("order_line.product_id", "=", self.product_id.id),
                    ])
                self.allowed_purchase_order_ids = [(6, 0, allowed_purchase.ids)]
                self.purchase_order_id = False

            if self.allowed_purchase_order_ids and len(self.allowed_purchase_order_ids) == 1:
                self.purchase_order_id = self.allowed_purchase_order_ids[0].id

            if self.allowed_sale_order_ids and len(self.allowed_sale_order_ids) == 1:
                self.sale_order_id = self.allowed_sale_order_ids[0].id

            if len(self.allowed_picking_ids) == 1:
                self.update({"picking_id": self.allowed_picking_ids[0]})


class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    picking_ids = fields.Many2many("stock.picking", string="Pickings")
    picking_type_id = fields.Many2one("stock.picking.type", string="Operation Type")
    allowed_product_ids = fields.Many2many(
        "product.product", string="Allowed Products"
    )
    show_so = fields.Boolean(default=False)
    show_po = fields.Boolean(default=False)

    def get_active_ids(self):
        active_ids = self.env.context.get("active_ids", [])
        if isinstance(active_ids, int):
            active_ids = [active_ids]
        return active_ids

    def _check_pickings_same_conditions(self, pickings):
        """
        Check if all pickings meet the following conditions:
        1. Same partner (customer/supplier).
        2. For SO: Same destination location.
           For PO: Same source location.
        3. Same operation type (picking type).
        """
        incompatible_pickings = []
        if not pickings:
            return False

        # Get the first picking's values for comparison
        first_picking = pickings[0]
        partner_id = first_picking.partner_id
        picking_type_id = first_picking.picking_type_id

        # Determine the location to compare based on the picking type
        if picking_type_id.code == "outgoing":  # SO
            location_to_compare = first_picking.location_dest_id
        elif picking_type_id.code == "incoming":  # PO
            location_to_compare = first_picking.location_id
        else:
            return False  # Only SO and PO are supported for multi-return

        # Compare with the rest of the pickings
        for picking in pickings:
            if(picking.state != "done" or picking.picking_type_id != picking_type_id):
                incompatible_pickings.append(picking.name)
            if (
                picking.partner_id != partner_id
                or (picking_type_id.code == "outgoing" and picking.location_dest_id != location_to_compare)
                or (picking_type_id.code == "incoming" and picking.location_id != location_to_compare)
            ):
                return False

        if len(incompatible_pickings)>0:
            message = _(
                "The selected transfer cannot be mass returned. Please check their states and operation types.\n\n"
                "Incompatibilities: %(incompatibilities)s",
                incompatibilities=" , ".join(incompatible_pickings),
            )
            raise UserError(message)
        return True

    @api.model
    def default_get(self, fields):
        active_ids = self.get_active_ids()
            
        if len(active_ids) == 1:
            return super().default_get(fields)

        res = super(models.TransientModel, self).default_get(fields)
        active_model = self.env.context.get("active_model")
        if active_model == "stock.picking" and active_ids:
            pickings = self.env["stock.picking"].browse(active_ids)
            if pickings.exists():
                # Validate that all pickings have the same partner and destination location
                if not self._check_pickings_same_conditions(pickings):
                    raise UserError(_("You can only return multiple pickings if they have the same partner and  location (customer or supplier)."))
                if pickings[0].picking_type_id.code == "outgoing":
                    res.update(
                        {
                            "show_so": True
                        }
                    )        
                if pickings[0].picking_type_id.code == "incoming":
                    res.update(
                        {
                            "show_po": True
                        }
                    )
                res.update(
                    {
                        "picking_ids": [(6, 0, pickings.ids)],
                        "picking_id": pickings[0].id,
                        "picking_type_id": pickings[0].picking_type_id.id,
                        "allowed_product_ids": [Command.set(pickings.mapped("move_ids.product_id").ids)],
                        "product_return_moves": [Command.clear()],
                    }
                )
        return res
      
    def _get_picking_ids(self):
        return self.product_return_moves.filtered(
            lambda line: line.quantity > 0
        ).mapped("picking_id")

    def action_create_returns(self):
        self.ensure_one()
        active_ids = self.get_active_ids()
        if len(active_ids) == 1:
            return super().action_create_returns()

        new_picking = self._create_return()
        self.picking_ids = self._get_picking_ids()
        last_message = self.env["mail.message"].search(
            [("res_id", "=", new_picking.id), ("model", "=", "stock.picking")],
            order="id desc",
            limit=1,
        )
        if last_message:
            last_message.unlink()
        new_picking.message_post_with_source(
            "mail.message_origin_link",
            render_values={"self": new_picking, "origin": self.picking_ids},
            subtype_xmlid="mail.mt_note",
        )
        origins = self.picking_ids.mapped("origin")
        origin = ", ".join(filter(None, origins))        
        vals = {
            "sale_id": self.picking_ids[0].sale_id.id,
            "sale_ids": self.picking_ids.mapped("sale_id").ids,
            "origin": _("Return of %(origins)s", origins=origin),
            "new_picking_ids": [(6, 0, self.picking_ids.ids)],
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

    def action_create_exchanges(self):
        """ Create a return for the active picking, then create a return of
        the return for the exchange picking and open it."""
        self.ensure_one()
        active_ids = self.get_active_ids()
        if len(active_ids) == 1:
            return super().action_create_exchanges()
        action = self.action_create_returns()
        proc_list = []
        origins = self.picking_ids.mapped("origin")
        origin = ", ".join(filter(None, origins))
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
            if self.picking_type_id.code == "outgoing":
                sale_orders = self.picking_ids.mapped("sale_id")
                if sale_orders:
                    new_pickings = self.env["stock.picking"].search(
                        [
                            ("origin", "=", origin),  # Match origins  
                            ("state", "=", "assigned"),  # Consider newly created pickings
                        ],
                        order="id desc",
                        limit=1,
                    )
                    # Assign multiple sale orders to the new pickings
                    if new_pickings and sale_orders:
                        new_pickings.write({'sale_ids': [(6, 0, sale_orders.ids)]})
        return action
