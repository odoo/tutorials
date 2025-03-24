from odoo import api, models, fields
from odoo.exceptions import UserError

class EstateAddOfferWizard(models.TransientModel):
    _name = 'estate.add.offer.wizard'
    _description = 'Wizard to add offers to multiple properties'

    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection([('new', 'New'), ('accepted', 'Accepted'), ('refused', 'Refused')], default='new', required=True, string="Offer Status", readonly=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_ids = fields.Many2many(
        'estate.property', 
        string="Selected Properties",
        default=lambda self: self._default_properties()
    )
    validity =fields.Integer("Validity (days)",default=7)


    @api.model
    def _default_properties(self):
        return self.env['estate.property'].browse(self.env.context.get('active_ids', []))

    def action_make_offer(self):
        if not self.property_ids:
            raise UserError("Please select at least one property.")

        for property in self.property_ids:
            if property.best_offer and self.price <= property.best_offer:
                raise UserError(f"Offer for {property.name} must be higher than {property.best_offer}")

            self.env['estate.property.offer'].create({
                'price': self.price,
                'status': self.status,
                'property_id': property.id,
                'validity': self.validity,
                'partner_id': self.buyer_id.id
            })
