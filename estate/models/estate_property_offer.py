from odoo import api, exceptions, fields, models, _


class PropertyOffers(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            date = fields.Date.today()
            if record.create_date:
                date = record.create_date.date()
            record.date_deadline = fields.Date.add(date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            record.property_id.offer_ids.status = "refused"
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_refuse(self):
        for record in self:
            record.status = "refused"

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "An offer price must be strictly positive.",
    )

    @api.model
    def create(self, vals_list):
        properties = self.env["estate.property"].browse(
            [vals.get("property_id") for vals in vals_list]
        )
        property_dict = {property.id: property for property in properties}
        for vals in vals_list:
            if property_dict[vals.get("property_id")].state == "sold":
                raise exceptions.ValidationError(
                    _("A new offer can't be made for an already sold property")
                )
            elif vals.get("price") < property_dict[vals.get("property_id")].best_price:
                raise exceptions.ValidationError(
                    _("A new offer can't have a lower amount than an existing offer")
                )
            property_dict[vals.get("property_id")].state = "offer_received"
        return super().create(vals_list)
