from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate properties offer"
    _order = "price desc"
    _sql_constraints = [
        ('check_offered_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'),
        ('refused', 'Refused')],
        help="Status of the offer", copy=False)
    validity = fields.Integer('Validity (days)', default='7')
    date_deadline = fields.Date('Deadline', 
        compute='_compute_date_deadline', 
        inverse='_inverse_date_deadline')
    partner_id = fields.Many2one(
        comodel_name='res.partner', required=True)
    property_id = fields.Many2one(
        comodel_name='estate.property', required=True)
    property_type_id = fields.Integer('Property Type ID', 
        related='property_id.property_type_id.id', store=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - base_date.date()).days

    @api.model
    def create(self, vals):
        property_record = self.env['estate.property'].browse(vals['property_id'])

        if property_record.state == 'sold':
            raise exceptions.UserError("You cannot create an offer for a sold property.")
        elif property_record.state == 'offer accepted':
            raise exceptions.UserError("Other offer has already been accepted for a property.")
        elif property_record.state == 'cancelled':
            raise exceptions.UserError("You cannot create an offer for a cancelled property.")
        elif int(vals['price']) < property_record.best_offer:
            raise exceptions.UserError(f"The offer must be higher than {property_record.best_offer}")
        else:
            property_record.state = 'offer received'

        return super(EstatePropertyOffer, self).create(vals)
    
    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            property = record.property_id
            for offer in property.offer_ids:
                if offer.id != record.id:
                    offer.status = 'refused'
            property.selling_price, property.buyer_id, property.state = record.price, record.partner_id, 'offer accepted'
                
    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
