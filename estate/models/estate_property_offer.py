from odoo import fields, api, models # type: ignore
from odoo.exceptions import ValidationError, UserError # type: ignore
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _sql_constraints = [
        ('check_offer_price','CHECK(price > 0)','Offer Price must be a positive amount')
    ]

    #-------------------------------------------Basic Fields-------------------------------------------#
    price = fields.Float(string="Price",required=True)
    state = fields.Selection(selection=[('accepted','Accepted'),('rejected','Rejected')],
                            string="State", copy=False
                            )
    validity = fields.Integer(string="Validity(days)", default=7)
    
    #-------------------------------------------Relational Fields---------------------------------------#
    partner_id = fields.Many2one("res.partner", string="Partner",required=True)
    property_id = fields.Many2one("estate.property",string="Property")
    
    #-------------------------------------------Computed Fields------------------------------------------#
    deadline_date=fields.Date(compute="_compute_deadline_date", inverse="_inverse_deadline_date", string="Deadline")

    # ------------------------------------------Compute Methods----------------------------------------#
    @api.depends("create_date", "validity")
    def _compute_deadline_date(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.deadline_date = date + relativedelta(days=offer.validity)

    def _inverse_deadline_date(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.deadline_date - date).days

    # --------------------------------------------Action Methods------------------------------------------------
    def offer_accept_action(self):
        for offer in self:
            if offer.state == "accepted":
                raise UserError('offer is already accepted')            
            offer.state = "accepted"
            offer.property_id.selling_price = self.price
            offer.property_id.buyer_id = self.partner_id
            return True
        
    def offer_reject_action(self):
        for offer in self:
            offer.state = "rejected"
            offer.property_id.selling_price = None
            offer.property_id.buyer_id = None
        return True
