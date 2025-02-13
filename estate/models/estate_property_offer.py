from datetime import timedelta  
from odoo import api,models, fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property offer'
    _order = "price desc"
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive.')
    ]

    price = fields.Float(string='Price', required=True)
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )

    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline",inverse="_inverse_date_deadline")
    validity = fields.Integer(string="Validity (days)", default=7)
    partner_id = fields.Many2one(
        "res.partner", string="Buyer", default=lambda self: self.env.user)
    property_id = fields.Many2one(
        'estate.property', string="Offer")
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type", related="property_id.property_type_id", store=True)

    def property_action_accept(self):
            if self.property_id.state == 'sold':
                raise UserError("Property already sold.")
            elif self.property_id.state == 'cancelled':
                raise UserError("Property cancelled, offers cannot be accept.")
            elif self.status == 'accepted':
                raise UserError("Buyer is already accepted.")

            for offer in self.property_id.offer_ids:
                    if offer.id != self.id:
                        offer.status = 'refused'

            self.status = 'accepted'
            self.property_id.write({
                'selling_price': self.price,
                'partner_id': self.partner_id.id,
                'state': 'offer_accepted'
            })

    def property_action_refuse(self):
        for record in self:
            record.status = 'refused'

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)
   
    
    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days if record.date_deadline else 7
            
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_obj = self.env["estate.property"].browse(vals["property_id"])

            existing_offer_prices = property_obj.offer_ids.mapped("price")
            new_offer_price = vals["price"]
            if existing_offer_prices and new_offer_price < max(existing_offer_prices):
                raise UserError("You cannot create an offer lower than an existing one.")

            property_obj.state = "offer_received"

        return super().create(vals_list)
