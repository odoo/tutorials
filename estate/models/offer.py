from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    estate_property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Estate Property",
        required=True,
    )
    price = fields.Monetary(string="Price", required=True, currency_field="currency_id")
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id
    )
    # STATUS AND DATE #
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        default=None,
        string="Offer Status",
    )

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )

    # USEFUL FOR DISPLAY #
    property_name = fields.Char("estate.property.type", related="estate_property_id.name")
    property_type_name = fields.Char("estate.property.type",
        related="estate_property_id.estate_property_type_id.name",
    )
    property_price = fields.Monetary("estate.property.type", related="estate_property_id.expected_price")
    property_postcode = fields.Char("estate.property.type", related="estate_property_id.postcode")
    property_type_id = fields.Many2one("estate.property.type", related="estate_property_id.estate_property_type_id", string="Property Type", store=True)

    ### CONSTRAINTS AND VALIDATION ###
    _check_expected_price_positive = models.Constraint(
        "CHECK(price > 0)",
        "Selling price must be positive",
    )

    @api.constrains("status", "estate_property_id")
    def _check_unique_accepted_offer(self):
        for offer in self:
            accepted_offers = offer.estate_property_id.offer_ids.filtered(
                lambda o: o.status == "accepted",
            )
            if len(accepted_offers) > 1:
                raise ValidationError(
                    _("You cannot have multiple accepted offers for the same property."),
                )

    ### COMPUTATED VALUES ###
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            days_to_add = record.validity or 0
            record.date_deadline = base_date + relativedelta(days=days_to_add)

    def _inverse_date_deadline(self):
        for o in self:
            o.validity = (o.date_deadline - o.create_date.date()).days

    ### ACTIONS ###
    def action_set_refused(self):
        for o in self:
            if o.status:
                raise UserError(_("This offer has already been %s", o.status))
            o.status = "refused"
        return True

    def action_set_accepted(self):
        for record in self:
            if record.estate_property_id.offer_ids.filtered(
                lambda o: o.status == "accepted",
            ):
                raise UserError(
                    _("An offer has already been accepted for this property."),
                )

            record.status = "accepted"
            record.estate_property_id.action_set_accepted()
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_by_user(self):
        for o in self:
            if o.status == "accepted":
                raise UserError(_("An accepted offer cannot be deleted."))
