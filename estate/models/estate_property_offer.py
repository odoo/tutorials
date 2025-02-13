from dateutil.relativedelta import relativedelta
from odoo.tools import float_compare

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "These are Estate Module Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ('check_price','CHECK(price > 0)', 'The offer price must be strictly positive!')
    ]

    price = fields.Float(string="price")
    state = fields.Selection(
        string="Status", 
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False
    )

    property_id = fields.Many2one(comodel_name="estate.property", string="Property", required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True)
    validity = fields.Integer(string="Validity (days)", default=7, compute="_compute_validity", inverse="_inverse_validity", store=True)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    property_type_id = fields.Many2one(comodel_name="estate.property.type", related="property_id.property_type_id", string="Property Type", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)


    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days


    @api.depends("create_date", "date_deadline")
    def _compute_validity(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days if offer.date_deadline else 7


    def _inverse_validity(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)


    def action_accept(self):
        if "accepted" in self.mapped("property_id.property_offer_ids.state"):
            raise UserError("An Offer is already been accepted")
        else:
            self.state = "accepted"
            self.property_id.state = "offer_accepted"
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price
        return True

    def action_refuse(self):
        self.state = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("property_id") and vals.get("price"):
                property = self.env["estate.property"].browse(vals["property_id"])
                best_price = property.best_price or 0.0
                if float_compare(vals["price"], best_price, precision_rounding=0.01) <= 0:
                    raise UserError("The offer price must be higher than %.2f" % best_price)
                property.state = "offer_received"

        return super().create(vals_list)
