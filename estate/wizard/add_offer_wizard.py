from odoo import models,fields,Command


class AddOfferWizard(models.TransientModel):
    _name = 'add.offer.wizard'
    _description = 'To create a offer for multipe properties simultaneously'

    price = fields.Integer()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
       )
    partner_id = fields.Many2one('res.partner', required=True, string='Buyer')

    def make_an_offer(self):
        active_ids = self.env.context.get('active_ids')
        all_properties = self.env['estate.property'].browse(active_ids)
        for property in all_properties:
            offer = property.offer_ids.create(
                {
                'property_id':property.id,
                'price' : self.price, 
                'partner_id' : self.partner_id.id,
                'status': self.status}
            )
            if(offer):
                if self.status == 'accepted':
                    offer.action_accepted()
                elif self.status == 'refused':
                    offer.action_refused()
        return False
