from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    state = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        help="Status of the Offer",
        copy=False,
    )
    validity = fields.Integer(string="Validity (days)", default=7)

    # region computed fields
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )
    # endregion

    # region relationships
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    # endregion

    # region constraints
    _check_price = models.Constraint(
        "CHECK(price > 0)", "The offer price must be strictly positive."
    )
    # endregion

    # region private methods
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date.date() if record.create_date else fields.Date.today()
            ) + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - date).days

    # endregion

    # region public methods
    def action_accept(self):
        for record in self:
            # not asked in the tutorial, but this prevents from having a UserError when clicking "Accept" on a already accepted offer
            other_offers = record.property_id.offer_ids - record
            if other_offers.filtered(lambda o: o.state == "accepted"):
                raise UserError(
                    self.env._("Only one offer can be accepted for a given property.")
                )
            record.state = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.state = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = [
            vals["property_id"] for vals in vals_list if vals.get("property_id")
        ]

        if property_ids:
            properties = self.env["estate.property"].search(
                [("id", "in", property_ids)]
            )
            properties_by_id = {prop.id: prop for prop in properties}

            for vals in vals_list:
                prop = properties_by_id.get(vals.get("property_id"))
                if prop and prop.offer_ids:
                    max_offer = max(prop.mapped("offer_ids.price"))
                    if vals.get("price", 0) <= max_offer:
                        raise UserError(
                            self.env._("The offer must be higher than %.2f", max_offer)
                        )
                    prop.state = "offer_received"

        return super().create(vals_list)


# endregion
