from odoo import models, fields


class EstateAddOfferWizard(models.TransientModel):

    _name = 'estate.add.offer.wizard'
    _description = 'estate add offer wizard'

    price = fields.Float(string='Price', required=True)
    status = fields.Selection(string='Status', selection=[
                              ('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one(comodel_name="res.partner", string="Buyer")

    def action_add_offer_wizard(self):
        properties = self.env['estate.property'].browse(self.env.context.get(
            "active_ids")).filtered_domain([('expected_price', '<=', self.price)])
        for rec in properties:
            current_offer = rec.offer_ids.create({
                'property_id': rec.id,
                'price': self.price,
                'partner_id': self.partner_id.id

            })
            if self.status == 'accepted':
                current_offer.action_accept()
            elif self.status == 'refused':
                current_offer.status = 'refused'
