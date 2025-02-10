#Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models,fields,api 
from datetime import date, timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    create_date = fields.Date(string="Creation Date", default=date.today())  
    validity = fields.Integer(string="Validity (Days)", default=7,store=True)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], string="Status", copy=False) 

    _sql_constraints = [
        ("check_offer_price", "CHECK(price > 0)", "The offer price must be strictly positive.")
    ]

    def action_accept(self):
        for record in self:
            if record.property_id.state == "sold":
                raise UserError("You cannot accept an offer for a sold property!")
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.state = "offer_received"
            record.property_id.selling_price =0.0

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else date.today()
            record.date_deadline = create_date + timedelta(days=record.validity) 

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else date.today()
            record.validity = (record.date_deadline - create_date).days if record.date_deadline else 7

