from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline"
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _check__price = models.Constraint(
        "CHECK(price > 0)",
        "The price of an offer must be strictly positive."
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(start_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start_date).days

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = self.env["estate.property"].browse(vals.get("property_id") for vals in vals_list)
        property_ids.mapped("offer_ids.price")
        property_map = {prop.id: prop for prop in property_ids}

        for vals in vals_list:
            property_record = property_map.get(vals.get("property_id"))
            if vals.get("price") <= property_record.best_price:
                raise UserError(self.env._("The offer must be higher than %s !", property_record.best_price))
        return super().create(vals_list)

    def action_accept_offer(self):
        self.ensure_one()
        for record in self:
            record.status = "accepted"
            for offer in record.property_id.offer_ids:
                if offer.id != record.id:
                    offer.status = "refused"
        return True

    def action_reject_offer(self):
        self.ensure_one()
        for record in self:
            record.status = "refused"
        return True
