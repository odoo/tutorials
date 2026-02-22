from odoo import models, fields


class EstateAccountInvoice(models.Model):
    _inherit = "account.move"

    property_id = fields.Many2one("estate.property", string="Property", copy=False)

    def action_view_property(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Property',
            'res_model': 'estate.property',
            'view_mode': 'form',
            'res_id': self.property_id.id,
            'target': 'current',
        }
