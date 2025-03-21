from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"


    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline",string="Deadline")
    state = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('sold', 'Sold'),
        ('refused', 'Refused'),
    ], string="Status", default="new")

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    property_type_id = fields.Many2one("estate.property.type", string="Property Type", related="property_id.property_type_id",
        store=True,
        readonly=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0 )',
         'An offer price must be strictly positive'),
          ('check_valid', 'CHECK(validity > 0 )',
         'An validity must be strictly positive')
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = date.today() + relativedelta(days=(record.validity))

    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline-record.create_date.date()).days

    def accept_offer(self):
        for record in self:
            record.state = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price=record.price
            record.property_id.buyer_id=record.partner_id

            other_offers = record.property_id.offer_ids - record
            other_offers.write({'state': 'refused'})
        return True

    def refuse_offer(self):
        for record in self:
            record.state = "refused"

        return True
    
    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            property_id = vals.get("property_id")
            offer_price = vals.get("price")

            if property_id:
                property = self.env["estate.property"].browse(property_id)

                if property.state == "offer_accepted":
                    raise UserError("Cannot make new offers. The property already has an accepted offer.")

                existing_offer_price = max(property.offer_ids.mapped("price"), default=0)

                if offer_price < existing_offer_price:
                    raise UserError("Offer price must be higher than existing offers!")

                property.state = "offer_received"

        return super().create(vals_list)
        