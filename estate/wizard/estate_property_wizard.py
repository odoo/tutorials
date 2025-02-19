from odoo import fields, models
from odoo.exceptions import UserError

class OfferWizard(models.Model):
    _name = "offer.wizard"
    _description = "This is a wizard to make offers"

    price = fields.Float(string=" Offer Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_ids = fields.Many2many('estate.property', string="Selected Properties")


    def action_make_offer(self):
        if not self.property_ids:
            raise UserError("No properties selected!")

        for property in self.property_ids:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'validity': self.validity,
                'partner_id': self.partner_id.id,
                'property_id': property.id,
            })
        return {'type': 'ir.actions.act_window_close'}
