from odoo import exceptions, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta

class RealEstatePropertyOfferWizard(models.TransientModel):
    _name = "real.estate.property.offer.wizard"
    _description = "Make offer in multiple properties"

    price = fields.Float(string = "Price", required = True)
    partner_id = fields.Many2one('res.partner', string = "Partner", required = True)
    validity = fields.Integer(string = 'Validity', required = True, default = 7)

    def action_save_offers(self):
        property_ids = self.env.context.get('active_ids')
        properties = self.env['real.estate.property'].browse(property_ids)
        for property_id in properties:
            try:
                self.env['real.estate.property.offer'].create({
                    'price': self.price,
                    'partner_id': self.partner_id.id,
                    'property_id': property_id.id,
                    'date_deadline': date.today() + relativedelta(days=self.validity),
                })
            except exceptions.UserError as e:
                raise e
            except Exception as e:
                raise UserError(
                    f"An unexpected error occurred while processing the offer for {property_id.name}: {str(e)}"
                )
        return True
