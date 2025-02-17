from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True, ondelete='cascade')
    property_type_id = fields.Many2one(related='property_id.property_type_id', string="Property Type")
    date_deadline = fields.Date(copy=False, default=fields.Date.today(), compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    validity = fields.Integer(default=7, store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            reference_date = record.create_date or fields.Datetime.now()
            record.date_deadline = fields.Date.add(fields.Date.from_string(reference_date), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            reference_date = record.create_date or fields.Datetime.now()
            reference_date = fields.Date.from_string(reference_date)
            if record.date_deadline:
                record.validity = (record.date_deadline - reference_date).days
    
    @api.constrains('property_id.expected_price')
    def _check_price(self):
        for record in self:
            if record.price < (record.property_id.expected_price*90/100):
                raise UserError("The offer price cannot be lower than 90% of the expected price.")
            else:
                record.accept_offer()

    def action_accept_offer(self):
        self.accept_offer()
        return True

    def accept_offer(self):
        # Check if there's already an accepted offer
        if self.property_id.state == 'offer_accepted':
            raise UserError("Another offer has already been accepted.")
        
        elif self.price < (self.property_id.expected_price*90/100):
            raise UserError("The offer price cannot be lower than 90% of the expected price.")
        
        else:
            # Refuse all other offers
            self.property_id.offer_ids.filtered(lambda o: o.id != self.id).write({
                'status': 'refused'
            })
            
            # Accept this offer and update property
            self.write({
                'status': 'accepted'
            })
            self.property_id.write({
                'selling_price': self.price,
                'buyer_id': self.partner_id.id,
                'state': 'offer_accepted'
            })
            return True
    
    def action_refuse_offer(self):
        # Reject this offer and update property
        self.write({
            'status': 'refused'
        })
        self.property_id.write({
            'selling_price': 1.0,
            'buyer_id': False,
            'state': 'new'
        })
        return True
    
    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        
        for offer in offers:
            property = offer.property_id

            # Check if the new offer is higher than existing ones
            existing_offers = property.offer_ids.filtered(lambda o: o.id != offer.id)
        if existing_offers:
            min_existing_price = min(existing_offers.mapped('price'))
            if offer.price < min_existing_price:
                raise UserError("The new offer price cannot be lower than the existing offer prices.")

        # Set 'offer_received' state only if it's the first offer
        if property.state == 'new' and not existing_offers:
            property.write({'state': 'offer_received'})

        return offers

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]
