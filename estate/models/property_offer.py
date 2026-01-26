from odoo import _, api, exceptions, fields, models


class PropertyOffer (models.Model):
    _name = "estate.property.offer"
    _description = "Property Purchase Offers"
    _order = "price desc"

    price = fields.Float(string="Price")
    property_id = fields.Many2one("estate.property", string="Property Name", required=True, ondelete="cascade")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", string="Property Type", store=True)
    status = fields.Selection(string="Status", selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    validity = fields.Integer(string="Validity", default="7")
    date_deadline = fields.Date(string="Deadline", compute="_compute_validity", inverse="_inverse_date")

    @api.depends("validity")
    def _compute_validity(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_confirm(self):
        for record in self:
            if not record.status:
                if record.property_id.status in ("sold", "cancelled", "offer accepted"):
                    err_msg = "This offer can not be accepted"
                    raise exceptions.UserError(err_msg)
                record.property_id.status = "offer accepted"
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.active = False
                record.property_id.partner_id = record.partner_id

        return True

    def action_cancel(self):
        for record in self:
            if not record.status:
                record.status = "refused"
        return True

    @api.constrains("price")
    def _check_price(self):
        for record in self:
            if record.price < 0:
                err_msg = "Enter a valid offer"
                raise exceptions.ValidationError(err_msg)
            if record.price < record.property_id.best_offer:
                err_msg = _("You can not enter an offer below %s") % record.property_id.best_offer
                raise exceptions.UserError(err_msg)

    @api.model
    def create(self, vals_list):
        offer = super().create(vals_list)
        offer.property_id.status = 'offer received'
        return offer
