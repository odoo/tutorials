from odoo import fields, models , api
from datetime import timedelta 
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Test Property"
    _order = "price desc" 

    price = fields.Float(string="Offer Price",required=True)
    status = fields.Selection(
        [('new','New'),('accepted','Accepted'),('refused','Refused')],
        default="new",
        string="Status"
    ) 
    partner_id = fields.Many2one('res.partner',string="Buyer",required=True)
    property_id = fields.Many2one('estate.property',string="Property",required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    ) 
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        related="property_id.property_type_id",
        store=True,
        string="Property Type",
    )
    _sql_constraints = [
        ('check_offer_price', 
         'CHECK(price > 0)', 
         'The offer price must be strictly positive!')
    ]  
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.selling_price:
                raise UserError("A selling price has already been set. You cannot accept another offer.")
            offer.status = 'accepted'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer = offer.partner_id

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
            offer.property_id.selling_price = 0
            offer.property_id.buyer = False 

    @api.model
    def create(self, vals_list):
        if "property_id" not in vals_list:
            raise UserError("Property ID is required to create an offer.")
        property = self.env["estate.property"].browse(vals_list["property_id"])
        existing_offer = self.search([("property_id", "=",vals_list["property_id"]),("price",">=",vals_list["price"])])
        if existing_offer:
            raise UserError("You cannot create an offer with a lower or equal amount than an existing offer.")
        if property.state == "new":
            property.state = "offer_received"
        return super(EstatePropertyOffer, self).create(vals_list)
