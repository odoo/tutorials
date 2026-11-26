from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Define offers for properties"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    buyer_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    can_be_accepted = fields.Boolean(compute="_compute_can_be_accepted")

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The price should be strictly positive',
    )

    @api.depends("property_id.state")
    def _compute_can_be_accepted(self):
        for record in self:
            record.can_be_accepted = record.property_id.state not in ("offer_accepted", "sold", "cancelled")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date or fields.Date.today(), days=record.validity)  # if validity is not set, it is treated as 0

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - (record.create_date or fields.Datetime.now()).date()).days
            else:
                record.validity = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            estate_property = self.env["estate.property"].browse(vals["property_id"])
            if estate_property.state in ("offer_accepted", "sold", "cancelled"):
                raise UserError(self.env._("You cannot make an offer on this property anymore."))
            if float_compare(vals.get("price", 0.0), estate_property.best_price, precision_digits=2) < 0:
                raise UserError(self.env._("The offer must be higher than %(price).2f.", price=estate_property.best_price))
        offers = super().create(vals_list)
        offers.mapped('property_id').filtered(lambda p: p.state == "new").state = "offer_received"
        return offers

    def action_accept(self):
        for record in self:
            match record.property_id.state:
                case "offer_accepted":
                    raise UserError(self.env._("An offer has already been accepted for this property."))
                case "sold":
                    raise UserError(self.env._("The property has already been sold."))
                case "cancelled":
                    raise UserError(self.env._("This property has been cancelled."))
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.buyer_id
            record.property_id.state = "offer_accepted"
            (record.property_id.offer_ids - record).status = "refused"

    def action_refuse(self):
        for record in self:
            record.status = "refused"
