import datetime
from odoo import api, fields, models, exceptions


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Define an offer on an property"
    _order = "price desc"
    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
        readonly=True
    )
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline")
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.estate.property", required=True)
    property_state = fields.Selection(related="property_id.state", readonly=True)
    property_type_ids = fields.Many2one(related="property_id.property_type_id", readonly=True, store=True)

    ## SQL Constraints Section ##

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price cannot be less than 0'
    )

    ## Methods Section ##

    def accept_offer_action(self):
        for record in self:
            if record.property_id.state == "cancelled" or record.property_id.state == "sold":
                raise exceptions.UserError("An offer on a sold or cancelled property cannot be accepted!")
            if record.status:
                raise exceptions.UserError("Cannot change the status of an already statued offer!")
            for offer in record.property_id.offer_ids:
                if offer.status == "accepted":
                    raise exceptions.UserError("Cannot have more than 1 accepted offer!")

            record.status = "accepted"
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    def refuse_offer_action(self):
        for record in self:
            if record.status:
                raise exceptions.UserError("Cannot change the status of an already statued offer!")
            else:
                record.status = "refused"
        return True

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if not record.create_date:
                record.date_deadline = fields.Date.today() + datetime.timedelta(days=record.validity)
            else:
                record.date_deadline = record.create_date + datetime.timedelta(days=record.validity)

    @api.depends("create_date", "date_deadline")
    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    ## CRUD Method ##
    @api.model
    def create(self, vals):
        existing_offers = self.search([("property_id", "=", vals[0]["property_id"])])
        for offer in existing_offers:
            if vals[0]["price"] <= offer.price:
                raise exceptions.UserError("The offer price cannot be lower than price of another offer!")
        property = self.env["estate.estate.property"].browse(vals[0]["property_id"])
        property.state = "offer_received"
        return super().create(vals)
