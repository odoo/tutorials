from odoo import fields, models


class EstatePropertyCancelWizard(models.TransientModel):
    _name = 'estate.property.cancel.wizard'
    _description = 'Property Cancellation Confirmation'

    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_name = fields.Char(string='Property Name', readonly=True)

    def action_confirm_cancel(self):
        """Confirm and execute cancellation"""
        self.property_id.action_cancel_property()
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel_wizard(self):
        """Cancel wizard without action"""
        return {'type': 'ir.actions.act_window_close'}
