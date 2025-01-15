
from odoo import fields, models, _

class EstatePropertyMakeOffer(models.TransientModel):
    _name = 'estate.property.make.offer'
    _description="To create a offer on multiple property"
    
    price= fields.Float(string="Price")
    partner_id= fields.Many2one(comodel_name="res.partner", required=True) #jha many2one hai fk vha store hoga
    validity= fields.Integer(string="Validity", default=7)

    
    def add_offer_to_property(self):
        property_ids= self.env.context['property_ids']
        failed_property_name=[]
        
        for property_id in property_ids:
            try:
                self.env['estate.property.offer'].create({
                    'price': self.price,
                    'validity': self.validity,
                    'property_id': property_id,
                    'partner_id': self.partner_id.id
                })
            except Exception:
                property_name = self.env['estate.property'].browse(property_id).name
                failed_property_name.append(property_name)

        if failed_property_name:
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Waning'),
                    'type': 'warning',
                    'message': f"Offered price is lower than 90% of best price hence skipping the offer addition for properties {failed_property_name}",
                    'sticky': False,
                    "next": {"type": "ir.actions.act_window_close"}
                }
            }
            return notification

        return {"type": "ir.actions.act_window_close"}
