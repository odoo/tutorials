from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
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
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", ondelete="cascade", required=True)
    validity = fields.Integer(default=7, string="Validity")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - base_date).days
  
    def action_accept(self):
        for record in self:
            if record.property_id.state == "sold" or record.property_id.state == "cancelled":
                raise UserError("sold or cancelled property's offer can't be accepted!")
            elif record.status == "accepted":
                raise UserError("Offer already Accepted!")
            elif 'accepted' in record.property_id.offer_ids.mapped('status'):
                raise UserError("Only one offer can be accepted for a property!")
            
            record.status = "accepted"

            record.property_id.write(
                {
                    'buyer': record.partner_id,
                    'selling_price': record.price,
                    'state': 'offer_accepted'
                }
            )
                  
    def action_refuse(self):
        for record in self:
            if record.property_id.state == "sold" or record.property_id.state =="cancelled":
                raise UserError("sold or cancelled property's offer can't be refused!")
            elif record.status == "accepted":
                record.property_id.write(
                    {
                        'buyer': '',
                        'selling_price': 0,
                        'state': 'new'
                    }
                )
            record.status = "refused"
  