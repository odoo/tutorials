# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError


class ContainerisationCreateWizard(models.TransientModel):
    _name = 'purchase.order.create.containerisation'
    _description = 'Wizard to create new container or add transfer into existing container.'

    add_to_existing = fields.Boolean(string='Add to Existing - I want to add these lines to an existing container transfer.')
    create_new_container = fields.Boolean(string='Create New - I want to create a new container transfer.', default=True)
    existing_container_id = fields.Many2one('stock.picking', string='Select a Container')
    destination_location_id = fields.Many2one('stock.location', string='Select a Destination Location')

    @api.onchange('add_to_existing')
    def _onchange_add_to_existing(self):
        if self.add_to_existing:
            self.create_new_container = False

    @api.onchange('create_new_container')
    def _onchange_create_new_container(self):
        if self.create_new_container:
            self.add_to_existing = False

    def action_confirm(self):
        active_ids = self.env.context.get('default_active_ids', [])
        selected_moves = self.env['stock.move'].browse(active_ids)
        if self.create_new_container:
            if not self.destination_location_id:
                raise UserError(_("Please select destination location to create container."))
            move_destinations = selected_moves.mapped('location_dest_id')
            if move_destinations and any(dest != self.destination_location_id for dest in move_destinations):
                selected_location_names = ", ".join(move_destinations.mapped('display_name'))
                warning_message = _(
                    "The selected moves have destination locations: %(selected_locations)s.\n"
                    "You have chosen a different destination: %(destination_location)s.\n\n"
                    "Do you want to continue?"
                )
                return {
                    "name": _("Location Mismatch"),
                    "type": "ir.actions.act_window",
                    "res_model": "containerisation.location.warning",
                    "view_mode": "form",
                    "target": "new",
                    "context": {
                        "default_warning_message": warning_message % {
                            "selected_locations": selected_location_names,
                            "destination_location": self.destination_location_id.display_name,
                        },
                        "default_container_wizard_id": self.id,
                        "default_supplier_id": self.env.context.get('default_supplier_id'),
                        "default_active_ids": active_ids,
                    },
                }
            return self.create_container(active_ids)
        elif self.add_to_existing:
            if not self.existing_container_id:
                raise UserError(_("Please select an existing container to add items."))
            existing_picking = self.existing_container_id
            move_destinations = selected_moves.mapped('location_dest_id')
            if any(move.location_dest_id != existing_picking.location_dest_id for move in selected_moves):
                selected_location_names = ", ".join(move_destinations.mapped('display_name'))
                warning_message = _(
                    "The selected moves have destination locations: %(selected_locations)s.\n"
                    "The existing container has a different destination: %(existing_destination)s.\n\n"
                    "Do you want to continue?"
                )
                return {
                    "name": _("Location Mismatch"),
                    "type": "ir.actions.act_window",
                    "res_model": "containerisation.location.warning",
                    "view_mode": "form",
                    "target": "new",
                    "context": {
                        "default_warning_message": warning_message % {
                            "selected_locations": selected_location_names,
                            "existing_destination": existing_picking.location_dest_id.display_name,
                        },
                        "default_container_wizard_id": self.id,
                        "default_existing_container_id": existing_picking.id,
                        "default_active_ids": selected_moves.ids,
                    },
                }
            return self.add_transfers_to_existing_container(selected_moves, existing_picking)

    def create_container(self, active_ids):
        selected_moves = self.env['stock.move'].browse(active_ids)
        warehouse = self.env['stock.warehouse'].search([
            ('lot_stock_id', '=', self.destination_location_id.id)
        ], limit=1)
        if not warehouse:
            picking_type = self.env.ref('purchase_order_containerisation.picking_type_containerisation')
        else:
            picking_type = self.env['stock.picking.type'].search([
                ('sequence_code', '=', 'IN/CONT'),
                ('warehouse_id', '=', warehouse.id)
            ], limit=1)
        picking = self.env["stock.picking"].create({
            "partner_id": self.env.context.get("default_supplier_id"),
            "picking_type_id": picking_type.id,
            "location_id": picking_type.default_location_src_id.id,
            "location_dest_id": self.destination_location_id.id,
            "move_ids": [Command.create({
                "product_id": move.product_id.id,
                "name": move.name,
                "product_uom_qty": move.quantity_to_containerise,
                "product_uom": move.product_uom.id,
                "location_id": move.location_id.id,
                "location_dest_id": move.location_dest_id.id,
                "move_orig_ids": [(4, move.id)],
                "purchase_line_id": move.purchase_line_id.id if move.purchase_line_id else False,
                "quantity_to_containerise": move.quantity_to_containerise
            }) for move in selected_moves],
            "state": "draft",
            "origin": ", ".join(filter(None, selected_moves.mapped("picking_id.origin"))) or "",
            "source_transfers": ", ".join(selected_moves.mapped("picking_id.name")) or "",
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'res_id': picking.id,
            'views': [(False, 'form')],
            'target': 'current',
        }

    def add_transfers_to_existing_container(self, selected_moves, existing_picking):
        existing_origins = set(filter(None, (existing_picking.origin or "").split(", ")))
        new_origins = set(filter(None, selected_moves.mapped('picking_id.origin')))
        merged_origins = ", ".join(existing_origins | new_origins)
        existing_sources = set(filter(None, (existing_picking.source_transfers or "").split(", ")))
        new_sources = set(filter(None, selected_moves.mapped('picking_id.name')))
        merged_sources = ", ".join(existing_sources | new_sources)
        move_commands = []
        for move in selected_moves:
            containerised_qty = move.quantity_to_containerise
            remaining_qty = move.product_uom_qty - containerised_qty
            if existing_picking.lifecycle_status == 'containerised':
                if remaining_qty == 0:
                    move.write({"product_uom_qty": remaining_qty, "state": 'cancel'})
                move.write({"product_uom_qty": remaining_qty})
            move_commands.append(Command.create({
                "product_id": move.product_id.id,
                "product_uom_qty": containerised_qty,
                "quantity": containerised_qty,
                "product_uom": move.product_uom.id,
                "picking_id": existing_picking.id,
                "name": move.name,
                "location_id": move.location_id.id,
                "location_dest_id": move.location_dest_id.id,
                "purchase_line_id": move.purchase_line_id.id if move.purchase_line_id else False,
                "move_orig_ids": [(4, move.id)],
                "quantity_to_containerise": containerised_qty,
            }))
        existing_picking.write({
            "move_ids": move_commands,
            "origin": merged_origins,
            "source_transfers": merged_sources,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'res_id': existing_picking.id,
            'views': [(False, 'form')],
            'target': 'current',
        }
