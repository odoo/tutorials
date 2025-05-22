from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An Offer on a property"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )

    validity = fields.Integer(string="Offer validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    # Relations
    property_id = fields.Many2one(comodel_name="estate.property", string="Property")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    partner_id = fields.Many2one("res.partner", string="Partner", copy=False)

    # -----------  BUSINESS LOGIC -------------- #

    @api.model_create_multi
    def create(self, vals_list):

        price, property_id = vals_list.get("price"), vals_list.get("property_id")

        if price and property_id:
            property = self.env["estate.property"].browse(property_id)
            if self._check_not_lowest_offer(price, property_id):
                property.set_offer_received()

        return super().create(vals_list)

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today(self) + relativedelta(days=10)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.date_deadline = fields.Date.today(self) + relativedelta(days=10)

    # -----------  MODELS ACTIONS  -------------- #

    def action_accept_offer(self):
        """ Accepts an offer on a property setting the states of offer and parent property """

        if self.property_id.state in ["offer_accepted", "sold"]:
            raise UserError("Can't accept 2 offers")

        self.write({
            "status": "accepted",
        })
        self.property_id.write({
            "selling_price": self.price,
            "state": "offer_accepted",
            "partner_id": self.partner_id,
        })

    def action_refuse_offer(self):
        """ Refuses an offer on a property setting the states of offer and parent property """

        self.write({
            "status": "refused",
        })
        self.property_id.write({
            "selling_price": 0.0,
            "partner_id": False,
        })

    # -----------  MODEL CONSTRAINTS  -------------- #

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price >= 0)', 'Offer price should be > 0'),
    ]

    # -----------  HELPERS  -------------- #

    def _check_not_lowest_offer(self, price, property_id):
        """Raise if price is lower than any existing offer."""

        Offer = self.env["estate.property.offer"]

        # Get the lowest offer for that property
        lowest_offer = Offer.search(
            [("property_id", "=", property_id)],
            order="price asc",
            limit=1,
        )

        if lowest_offer and price < lowest_offer.price:
            raise ValidationError("Can't create an offer lower than an existing offer ")

        return True
