from odoo import exceptions, fields, models

class EstateWizard(models.TransientModel):
    _name='wizard.estate.property'
    _description='Estate TransientModel Wizard'

    price = fields.Float('Price')
    partner_id = fields.Many2one('res.partner', string="Buyers")
    validity = fields.Integer(string='Validity(day)', default='7')

    def action_add_offer(self):
        property_ids = self.env['estate.property'].browse(self.env.context.get('active_ids', []))
        if property_ids:
            result = []
            for property in property_ids:
                if property.state in ['new', 'offer_received'] and property.best_price <= self.price :
                    result.append({
                            'price': self.price,
                            'property_id': property.id,
                            'validity': self.validity,
                            'partner_id': self.partner_id.id,
                    })

            self.env['estate.property.offer'].create(result)
