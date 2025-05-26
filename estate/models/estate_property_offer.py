from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


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

        for val in vals_list:

            price, property_id = val.get("price"), val.get("property_id")

            if price and property_id:
                property = self.env["estate.property"].browse(property_id)

                if float_compare(price, property.best_offer, 2) == -1:
                    raise ValidationError("Can't create an offer lower than best offer")
                else:
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
        """ Refuses an offer on a property """
        self.write({
            "status": "refused",
        })

    # -----------  MODEL CONSTRAINTS  -------------- #

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price >= 0)', 'Offer price should be > 0'),
    ]
