from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "It is a estate property offer model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refuse", "Refuse")], copy=False
    )

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_date_validity"
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(
                fields.Date.to_date(create_date), days=record.validity
            )

    def _inverse_date_validity(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.validity = (
                record.date_deadline - fields.Date.to_date(create_date)
            ).days

    def action_offer_accept(self):
        self.status = "accepted"
        records = self.property_id.offer_ids
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"

        for record in records:
            if self.id != record.id:
                record.status = "refuse"

    def action_property_refuse(self):
        self.status = "refuse"

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price of property must be positive",
    )

    @api.model_create_multi
    def create(self, vals_list):
        if vals_list:
            property_id = self.env["estate.property"].browse(
                vals_list[0].get("property_id")
            )
            best_price = property_id.best_price
            for vals in vals_list:
                if vals.get("price") < best_price:
                    raise UserError(
                        self.env._("Offer price can't be less than %s", best_price)
                    )

            property_id.state = "offer_received"

        return super().create(vals_list)

    @api.constrains("validity")
    def _check_validity_and_create_date(self):
        for record in self:
            if record.validity < 0:
                raise UserError(self.env._("Invalid validity period."))

    @api.ondelete(at_uninstall=False)
    def unlink_offer(self):
        if len(self.property_id.offer_ids) == len(self):
            self.property_id.state = "new"
