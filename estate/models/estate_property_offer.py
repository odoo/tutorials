from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    # Fields declaration
    price = fields.Float("Price")
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline" )
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store="True" ,string="Property Type")
     # SQL constraints
    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price >= 0)",
            "The price must be strictly positive.",
        )
    ]

    # Compute and inverse methods in order of field declaration
    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or fields.Datetime.today()) + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = fields.Date.from_string(offer.create_date)
            offer.validity = (offer.date_deadline - create_date).days

    # Action methods
    def action_offer_confirm(self):
        if self.property_id.state in ("new", "offer_received"):
            self.status = "accepted"
            self.property_id.partner_id = self.partner_id
            self.property_id.selling_price = self.price
            self.property_id.state = "offer_accepted"
        else:
            raise UserError("you can select only one offer for one property.")
        

    def action_offer_cancel(self):
        self.status = "refused"
        self.property_id.partner_id = ""
        self.property_id.selling_price = 0
        self.property_id.state = "offer_received"
    
    @api.model_create_multi
    def create(self, vals_list):
      
        for vals in vals_list:
            # Validate that the new offer amount is greater than existing offers
            property_id = self.env["estate.property"].browse(vals.get("property_id"))
            if property_id.best_price >= vals["price"]:
                raise UserError(
                    "You cannot create an offer with an amount lower than or equal to an existing offer.")
            else:
                property_id.state = "offer_received"

        return super(EstatePropertyOffer, self).create(vals_list)
  