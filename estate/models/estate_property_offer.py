from odoo import fields,models,api,_
from odoo.exceptions import UserError
from datetime import timedelta,datetime

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Offers of Estate Property"
    _order = 'price desc'

    _check_offer_price = models.Constraint('CHECK(price > 0)','The Offer price must be positive.')

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id = fields.Many2one('res.partner',string="Partner",required=True)
    property_id = fields.Many2one('estate.property',string="Property",required=True)
    property_type_id = fields.Many2one(
    'estate.property.types',
    related="property_id.property_type_id",
    string="Property Type",
    required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline",inverse="_inverse_deadline",store=True)
    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date or datetime.now()
            record.date_deadline = create_date + timedelta(days=record.validity)
    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date or datetime.now()    
            if record.date_deadline:
                delta = record.date_deadline - create_date.date()
                record.validity = delta.days
    
    def action_accept_offer(self):
        for record in self:
            existing = self.search([
                ('property_id','=',record.property_id.id),
                ('status','=','accepted')
            ])
            if existing:
                raise UserError(_("Another offer has been already accepted."))
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id.id
    def action_refuse_offer(self):
        for record in self:
            if(record.status == 'accepted'):
                raise UserError(_("Accepted Offer cannot be Refused"))
            else:
                record.status = "refused"

