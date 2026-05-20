from odoo import api, fields, models 
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _order = 'price desc'

    price = fields.Float(required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True)

    # SQL constraints
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        "An offer price must be strictly positive."
    )

    # Compute and inverse methods
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = fields.Date.add(base_date, days=offer.validity)
            
    def _inverse_date_deadline(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - base_date).days

    # CRUD methods       
    @api.model
    def create(self, vals):   
        for val in vals:
            property_id = val.get('property_id')
            if property_id:
                property_record = self.env['estate.property'].browse(property_id)

                if property_record.state == 'cancelled':
                    raise UserError("An offer cannot be made for a cancelled property!")

                for existing_offer in property_record.offer_ids:
                        if val.get('price', 0) < existing_offer.price:
                            raise UserError("The offer amount cannot be lower than an existing offer!")

                property_record.state = 'offer_received'

        return super().create(val)

    # Action methods
    def action_accept(self):
        for offer in self:
            if offer.property_id:
                if offer.property_id.buyer_id:
                    raise UserError("An offer has already been accepted!")
                    
                offer.status = 'accepted'
                offer.property_id.buyer_id = offer.partner_id
                offer.property_id.selling_price = offer.price
                offer.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
            if offer.property_id and offer.property_id.buyer_id == offer.partner_id:
                    offer.property_id.buyer_id = False
                    offer.property_id.selling_price = 0.0
        return True
        