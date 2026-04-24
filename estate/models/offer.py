from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    estate_property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Estate Property",
        required=True,
    )
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        default=None,
        string="Offer Status",
    )

    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )

    property_name = fields.Char(related="estate_property_id.name")
    property_type_name = fields.Char(
        related="estate_property_id.estate_property_type_id.name",
    )
    property_price = fields.Float(related="estate_property_id.expected_price")
    property_postcode = fields.Char(related="estate_property_id.postcode")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for o in self:
            if o.create_date:
                o.date_deadline = fields.Date.add(
                    o.create_date,
                    days=o.validity,
                )
            else:
                o.date_deadline = fields.Date.add(fields.Date.today(), days=o.validity)

    def _inverse_date_deadline(self):
        for o in self:
            o.validity = (o.date_deadline - o.create_date.date()).days

    def action_set_accepted(self):
        # todo: split action and validation (validation goes into python constraint)
        for o in self:
            accepted_offers_for_property = o.estate_property_id.offer_ids.filtered(
                lambda o: o.status == "accepted",
            )
            if (
                len(accepted_offers_for_property) == 1
                and accepted_offers_for_property[0] != o
            ):
                raise UserError(
                    _("There is already an accepted offer for that property."),
                )

            if o.estate_property_id.state in {"cancelled", "sold", "offer_accepted"}:
                raise UserError(
                    _(
                        "Property status does not allow to accept the offer. Current status is %s",
                        o.estate_property_id.state,
                    ),
                )
            if o.status:
                raise UserError(_("This offer has already been %s", o.status))

            o.status = "accepted"
            o.estate_property_id.action_set_accepted()
        return True

    def action_set_refused(self):
        # todo: split action and validation (validation goes into python constraint)
        for o in self:
            if o.status:
                raise UserError(_("This offer has already been %s", o.status))
            o.status = "refused"
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_by_user(self):
        for o in self:
            if o.status == "accepted":
                raise UserError(_("An accepted offer cannot be deleted."))
            super().unlink()
