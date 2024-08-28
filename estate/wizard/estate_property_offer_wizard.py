from odoo import models, fields
from odoo.exceptions import ValidationError


class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'this is the wizard which allows to make offers for multiple propertie at the same time'

    price = fields.Float(string='Offer Price', required=True)
    offer_status = fields.Selection(
        string='Status',
        selection=[('received', 'Received'), ('accepted', 'Accepted'), ('refused', 'Refused')],
        copy="False",
        help="Status of the Offer",
        default='received')
    buyer_id = fields.Many2one('res.partner', string='Buyer', required=True)

    def add_offer_action(self):
        self.ensure_one()
        property_ids = self.env.context.get('active_ids', [])
        estate = self.env['estate.property'].browse(property_ids).filtered_domain([('expected_price', '<=', self.price), ('property_type_id.name', '=', 'flat')])

        for property_id in estate:
            if property_id.state in ['offer accepted', 'sold', 'cancelled']:
                raise ValidationError("Cannot make an offer on property")
            else:
                offer = self.env['estate.property.offer'].create({
                        'property_id': property_id.id,
                        'price': self.price,
                        'status': self.offer_status,
                        'partner_id': self.buyer_id.id
                        })
                if self.offer_status == 'accepted':
                    offer.action_accept_button()
                else:
                    offer.action_refuse_button()
