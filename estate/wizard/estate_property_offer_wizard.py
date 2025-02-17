from odoo import models, fields
from odoo.exceptions import UserError

class EstatePropertyOfferwizard(models.TransientModel):

    _name = "estate.property.offer.wizard"
    _description = "Wizard for Estate Property Offer"

    price = fields.Float(string="Price", required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Buyer", required=True)


    def action_make_offer(self):
        properties = self.env['estate.property'].browse(self._context.get('active_ids', []))

        valid_properties = properties.filtered(lambda p: p.state in ['new', 'offer_received'])
        if not valid_properties:
            raise UserError("No valid properties found for making offers.")

        self.env['estate.property.offer'].create([
            {'price': self.price, 'partner_id': self.partner_id.id, 'property_id': p.id}
            for p in valid_properties
        ])

        return {'type': 'ir.actions.act_window_close'}
