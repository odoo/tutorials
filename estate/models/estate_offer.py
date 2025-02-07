from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError

class EstateOffer(models.Model):
    _name = 'estate.property.offer' 
    _description = 'Offer'

    price = fields.Float(string="Price", required=True)
    status_offer = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", default='new', copy=False)  

    _order = "id desc"

    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer(string="Validity (Days)", store=True)
    date_deadline = fields.Date(string="Date-Deadline", compute="_compute_date_deadline", inverse="_set_date_deadline", store=True)


    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price<=0:
                raise ValidationError("price should strictly be positive")

    _sql_constraints = [
        ("check_offer_price", "CHECK (price > 0)", "Offer price should strictly be positive")
    ]


    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """ Compute date_deadline based on create_date and validity. """
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _set_date_deadline(self):
        """ Inverse function to set validity based on date_deadline """
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
            else:
                record.validity = 7  # Default validity if no date_deadline is set

    def accept_offer(self):
        """ Accept an offer """
        for record in self:
            record.status_offer = "accepted"
            record.property_id.selling_price=record.price
            record.property_id.property_buyer_id=record.partner_id
        return True

    def reject_offer(self):
        """ Reject an offer """
        for record in self:
            record.status_offer = "refused"
            record.property_id.selling_price=0.000
        return True
