from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price desc"
    _sql_constraints = [
        ('check_price', 'CHECK(price>0)', 'The offer price must be strictly positive!')
    ]

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection = [
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ]
    )
    partner_id = fields.Many2one(
        "res.partner", string="Buyer", required=True
    )
    property_id = fields.Many2one(
        "estate.property", string="Property", ondelete="cascade", required=True
    )
    validity = fields.Integer(default=7, string="Validity")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    property_type_id = fields.Many2one(
        "estate.property.type" , related="property_id.property_type_id", store=True
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - base_date).days
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_obj = self.env['estate.property'].browse(vals['property_id'])
            
            if property_obj.state == "new":
                property_obj.state = 'offer_received'

            existing_offer = self.search([
                ('property_id', '=', vals.get('property_id'))
            ], order="price desc", limit=1)

            if existing_offer and vals.get('price') < existing_offer.price:
                raise ValidationError("You can't create an offer lower than an existing one.")
            
        return super().create(vals_list)
    
    def unlink(self):
        for offer in self:
            property_obj = offer.property_id

            super(EstatePropertyOffer, offer).unlink()

            remaining_offers = self.search_count([('property_id', '=', property_obj.id)])
            if remaining_offers == 0:
                property_obj.state = 'new'
  
    def action_accept(self):
        for record in self:
            if record.property_id.state == "cancelled":
                raise UserError("Cancelled property's offer can't be accepted!")
            
            record.status = "accepted"

            remaining_offers = self.search([
                ('id', '!=', record.id), ('property_id', '=', record.property_id.id)
            ])
            if remaining_offers:
                remaining_offers.write({'status' : 'refused'})

            record.property_id.write(
                {
                    'buyer_id': record.partner_id,
                    'selling_price': record.price,
                    'state': 'offer_accepted'
                }
            )
                  
    def action_refuse(self):
        for record in self:
            if record.property_id.state =="cancelled":
                raise UserError("Cancelled property's offer can't be refused!")
            record.status = "refused"
