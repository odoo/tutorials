from odoo import _,fields,models


class MakeBulkOffer(models.TransientModel):
    _name = 'estate.property.make.bulk.offer'
    _description = 'Make Bulf Offer for Properties at once'
    
    price = fields.Float('Property Price')
    validity=fields.Integer('Validity (days)', default=7 )
    partner_id = fields.Many2one('res.partner', string='Partner',required=True , ondelete="cascade")

    def make_offers(self):
        property_failed = []
        for property in self.env.context.get("active_ids"):
            try:
                self.env['estate.property.offer'].create({
                    'price': self.price,
                    'property_id': property,
                    'partner_id': self.partner_id.id,
                    'validity': self.validity
                })

            except Exception:
                property_failed.append(self.env['estate.property'].browse(property).name)

        if property_failed:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'danger',
                    'message': _("Offers have not been applied to following properties %s.", ', '.join(property_failed)),
                    'next': {
                        "type": "ir.actions.act_window_close"
                    }
                }
            }
