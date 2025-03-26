# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models
from odoo.exceptions import UserError


class ContainerisationLocationWarning(models.TransientModel):
    _name = 'containerisation.location.warning'
    _description = 'Wizard to display warning when the destination location of container and destination location of the selected transfer is mismatched.'

    warning_message = fields.Char(string='Warning Message', readonly=True)
    container_wizard_id = fields.Many2one('purchase.order.create.containerisation', string='Container Wizard')
    existing_container_id = fields.Many2one('stock.picking', string='Existing Container')
    active_ids = fields.Many2many('stock.move', string='Selected Moves')

    def action_continue(self):
        if not self.container_wizard_id:
            raise UserError(_("Container wizard reference is missing."))
        selected_moves = self.env['stock.move'].browse(self.active_ids.ids)
        if self.existing_container_id:
            return self.container_wizard_id.add_transfers_to_existing_container(selected_moves, self.existing_container_id)
        else:
            return self.container_wizard_id.create_container(self.active_ids.ids)

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
