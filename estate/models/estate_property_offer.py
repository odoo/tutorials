from odoo import api,models, fields
from datetime import timedelta  
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property offer'
    _order = "price desc"
    
    price = fields.Float(string='Price', required=True)
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", default=lambda self: self.env.user)
    property_id = fields.Many2one('estate.property', string="Offer")
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline",inverse="_inverse_date_deadline")
    validity = fields.Integer(string="Validity (days)", default=7)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", related="property_id.property_type_id", store=True)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)
   
    
    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days if record.date_deadline else 7

    def property_action_accept(self):
            if self.property_id.state == 'sold':
                raise UserError("Property already sold.")
            elif self.property_id.state == 'cancelled':
                raise UserError("Property cancelled, offers cannot be accept.")
            elif self.status == 'accepted':
                raise UserError("Buyer is already accepted.")
            else:
                for offer in self.property_id.offer_ids:
                    if offer.id != self.id:
                        offer.status = 'refused'
                    else:
                        self.write({'status': 'accepted'})
                        self.property_id.write({
                            'selling_price': self.price,
                            'buyer_id': self.partner_id,
                            'state': 'offer_accepted'
                        })

    def property_action_refuse(self):
        for record in self:
            record.status = 'refused'

    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)
            
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive.')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_obj = self.env["estate.property"].browse(vals["property_id"])

            existing_offer_prices = property_obj.offer_ids.mapped("price")
            if existing_offer_prices and self.price < max(existing_offer_prices):
                raise UserError("You cannot create an offer lower than an existing one.")

            property_obj.state = "offer_received"

        return super().create(vals_list)
