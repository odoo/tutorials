from odoo import fields,api,models
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
#-----------------------------------------------Basic Fields-------------------------------------------#
    price = fields.Float(string="Price",required=True)
    state = fields.Selection(selection=[('accepted','Accepted'),('rejected','Rejected')],
                            string="State", copy=False
                            )
    validity = fields.Integer(string="Validity(days)", default=7)
    
    #-------------------------------------------Relational Fields---------------------------------------#
    seller_id = fields.Many2one("res.partner", string="Salesman",required=True)
    property_id = fields.Many2one("estate.property",string="Property")
    
    #-------------------------------------------Computed Fields------------------------------------------#
    deadline_date=fields.Date(compute="_compute_deadline_date", inverse="_inverse_deadline_date", string="Deadline")

    # ------------------------------------------Decorator Methods----------------------------------------#
    @api.depends("create_date", "validity")
    def _compute_deadline_date(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.deadline_date = date + relativedelta(days=offer.validity)

    def _inverse_deadline_date(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.deadline_date - date).days
