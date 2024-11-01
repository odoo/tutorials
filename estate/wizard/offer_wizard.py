from odoo import fields, models


class offerWizard(models.TransientModel):
    _name = "offer.wizard"

    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    property_id = fields.Many2one('estate.property', string="Property")

    def action_offer_add(self):
        active_ids = self._context.get('active_ids')
        property = self.env['estate.property'].browse(active_ids)
        for prop in property:
            p = {'price': self.price, 'status': self.status, 'partner_id': self.partner_id.id, 'property_id': prop.id}
            self.env['estate.property.offer'].browse(prop).create(p)
        return True
