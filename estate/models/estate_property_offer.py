from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

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
            if "accepted" in other_offers.mapped("state"):
                raise UserError(
                    _("Only one offer can be accepted for a given property.")
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

    # endregion
