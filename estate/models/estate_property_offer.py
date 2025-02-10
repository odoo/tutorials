from odoo import models,fields,api
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Real Estate Property Offer Model"

    price=fields.Float(required=True,copy=False,default=0)
    status=fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id=fields.Many2one('res.partner',required=True)
    property_id=fields.Many2one('estate.property',required=True)
    validity=fields.Integer(string="Validity (in days)",default=7)
    date_deadline=fields.Date(compute='_compute_date_deadline',inverse='_inverse_date_deadline',string="Deadline")

    _sql_constraints=[('offer_price_positive','CHECK(price>0)','Price must be positive number')]

    # Computation methods
    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            record.create_date=record.create_date or fields.Datetime.today()
            record.date_deadline= record.create_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.create_date= record.create_date or fields.Datetime.today()
            record.validity=(record.date_deadline-record.create_date.date()).days

    # Action methods
    def action_accept(self):
        if any(offer.status=="accepted" for offer in self.property_id.offer_ids):
            raise UserError("Offer already accepted.")
        self.write({'status':"accepted"})
        self.property_id.write({'selling_price':self.price})
        self.property_id.write({'buyer_id':self.partner_id})

    def action_refuse(self):
        self.write({'status':"refused"})
        if any(offer.status=="accepted" for offer in self.property_id.offer_ids):
            return
        self.property_id.write({'selling_price':False})
        self.property_id.write({'buyer_id':False})
        return True

    # Constraint methods
    @api.constrains('price')
    def _check_price(self):
        compare_value = float_compare(self.price,0.9*self.property_id.expected_price,precision_digits=2)
        if compare_value == -1:
                raise UserError("Offer Price must be atleast 90% of the expected price.")
        return True
