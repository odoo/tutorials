from odoo import fields, models
from odoo.exceptions import UserError

class EstateAddOfferWizard(models.TransientModel):
    _name = 'estate.property.add.offer.wizard'
    _description = 'Wizard to add offer to multiple estate properties'

    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=14)
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)

    def action_make_offer(self):
        active_ids = self.env.context.get('active_ids', [])

        if not active_ids:
            raise UserError("No properties selected.")

        failed_count = 0
        for property_id in active_ids:
            try:
                self.env['estate.property.offer'].create({
                    'price': self.price,
                    'validity': self.validity,
                    'partner_id': self.partner_id.id,
                    'property_id': property_id,
                })
            except Exception as e:
                failed_count += 1

        # Show notification and close wizard
        if failed_count > 0:
            self.env.cr.commit()  # Commit successful offers
            message = f'Offer creation failed for {failed_count} properties.'
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': message,
                    'type': 'warning',
                    'sticky': True,
                    'next': {'type': 'ir.actions.act_window_close'},
            },}

        return {'type': 'ir.actions.act_window_close'}
