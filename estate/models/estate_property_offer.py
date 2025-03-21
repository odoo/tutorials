from datetime import date, datetime, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"  # Descending order of price

    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    validity_date = fields.Date(string="Validity Date", compute="_compute_validity_date", inverse="_inverse_validity_date", store=True) # used store because assuming we have filter of validity date then it will directly take from db, otherwise it have to calculate each time.
    # store = true, not needed when it uses for only display, (not for sorting or searching) at that time we can ignore it.
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one(
    'estate.property', 
    string="Property",
    required=True, 
    ondelete="cascade"
)   # if I set ondelete = "set null" then why it is not taking and giving error -- 
    #The m2o field property_id of model estate.property.offer is required but declares its ondelete policy as being 'set null'. 
    # Only 'restrict' and 'cascade' make sense
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", copy=False)
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    @api.depends("validity")
    def _compute_validity_date(self):
        for record in self:
            record.validity_date = record.create_date + timedelta(days=record.validity) if record.create_date else date.today()

    def _inverse_validity_date(self):
        for record in self:
            if record.validity_date and record.create_date:
                record.validity = (record.validity_date - record.create_date.date()).days

    def action_accept(self):
        if self.property_id.state in ["offer_accepted", "sold"]:
            raise UserError("Cannot accept offers for a sold property or one with an accepted offer.")

        self.property_id.selling_price = self.price
        self.property_id.state = "offer_accepted"
        self.property_id.buyer_id = self.partner_id
        self.status = "accepted"
        # return True

    def action_refuse(self):
        if self.status == "accepted":
            self.property_id.selling_price = 0
            self.property_id.state = "offer_received"
            self.property_id.buyer_id = False
        
        self.status = "refused"
        # return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list :
            property_obj = self.env['estate.property'].browse(vals['property_id'])
        # Check if the offer is lower than the existing highest offer
            existing_offers = property_obj.mapped("offer_ids.price")
            if existing_offers and vals['price'] < max(existing_offers):
                raise exceptions.UserError("You cannot create an offer lower than an existing offer.")
        # Set property state to 'Offer Received'
            if property_obj.state == 'new':
                property_obj.state = 'offer_received'

        return super().create(vals_list)
