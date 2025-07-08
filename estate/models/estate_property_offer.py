



# offers model that will offer us the offers 



from odoo import fields, models, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer model for the properties of real estate'
    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused ')],
        string='Status',
        copy = False
    )

    partner_id = fields.Many2one('res.partner', string = 'Partner')

    property_id = fields.Many2one('estate.property', string ='Property')

    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id",store=True,readonly=False)
    
    validity = fields.Integer(default= 7)

    date_deadline = fields.Date(compute = '_compute_offer_deadline', inverse = '_deadline_update')

    
    # constrains of sql

    _sql_constraints = [('check_price', 'CHECK(price > 0)', 'Offered price must be strictly positive')
    ]
   
   # order in which data is fetched

    _order = "price desc"



    # deadline will be computed based upon the validity date
    @api.depends('validity')
    def _compute_offer_deadline(self):
        for offer in self:
            if not offer.create_date:
                offer.date_deadline = datetime.now() + relativedelta(days=(offer.validity or 0))
                return

        offer.date_deadline = offer.create_date + relativedelta(days=(offer.validity or 0))
        

    # deadline date can also be changed and once this is saved validity will be updated
    def _deadline_update(self):
        for offer in self:
            offer.validity = (offer.date_deadline - (offer.create_date or datetime.now()).date()).days
       

    # action for the accepting the offer 
    def action_offer_confirm(self):
        for record in self:
            # since saling price is only updated when offer is accepted therefore it validates if offer 
            # is already accepted than warning

           if record.property_id.selling_price > 0 :
                raise UserError('Offer price already accepted for the property')

        record.status = 'accepted'
        record.property_id.selling_price = self.price
        record.property_id.partner_id = record.partner_id
        record.property_id.state = 'offer_accepted'

    # action for the refusal of the status
    def action_offer_refuse(self):

        for record in self:
            if (record.status == 'accepted'): 
                record.property_id.selling_price = 0
                record.property_id.partner_id = ''
            record.status = 'refused'


    