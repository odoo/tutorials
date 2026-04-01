from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer module for Odoo 19 tutorials"
    _order = "price desc"

    price = fields.Float(required=True, string="Offer Price")
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], copy=False, string="Offer Status")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (in days)", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline", store=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True, string="Property Type")

    _check_offer_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            current_property = self.env["estate.property"].browse(val["property_id"])
            if val["price"] < current_property.best_price:
                raise UserError(_("An offer with higher price already exists"))
            current_property.state = "offer_received"
        return super().create(vals_list)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date.date(), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def _cron_validity_reject(self):
        self.search([('status', '=', False), ('date_deadline', '<', fields.Date.today())]).action_refuse()

    def action_accept(self):
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped("status"):
            raise UserError(_("Offer already accepted"))

        self.status = "accepted"
        self.property_id.state = "offer_accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        remaining_offers = self.property_id.offer_ids - self
        remaining_offers.action_refuse()

    def action_refuse(self):
        self.status = "refused"
