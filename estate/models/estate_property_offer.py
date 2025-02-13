from odoo import api,fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted','Accepted'),
                    ('refused','Refused')],
        copy=False,
    )
    validity = fields.Integer(default="7")
    date_deadline = fields.Date(compute="_compute_date_deadline",inverse="_inverse_date_deadline",store=True)

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Properties", required=True, ondelete="cascade")
    property_type_id = fields.Many2one("estate.property.type", string="Property Types", store=True)

    _sql_constraint = [
        ('check_pos_offer_price','CHECK(price > 0)','Offered price should be greater than 0')
    ]

    @api.depends("validity","create_date")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            record.date_deadline = timedelta(record.validity) + create_date.date()

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
    
    def action_accept_offer(self):
        if self.property_id.state in ['sold', 'cancelled']:
            raise UserError("A sold or cancelled property cannot accept anyother offer.")
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'
        self.property_id.buyer_id = self.partner_id
        other_offers = self.property_id.offer_ids - self
        other_offers.write({'status':'refused'})
        return True

    def action_refuse_offer(self):
        self.status = 'refused'
        self.property_id.state = 'offer_recieved'
        self.property_id.selling_price = False
        self.property_id.buyer_id = False
        return True

    @api.model_create_multi
    def create(self, vals_list):
        property = self.env['estate.property'].browse(vals_list['property_id'])
        if property.best_price>0: #if list is empty, initial condition.
            if vals_list['price'] <= max(property.offer_ids.mapped("price")):
                raise UserError("Create an offer with a higher price than an existing offer.")
        property.state = 'offer_recieved'
        return super().create(vals_list) 
    