from dateutil.relativedelta import relativedelta

from odoo import api, exceptions, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate model"
    _order = "id desc"

    name = fields.Char(required=True)
    salesman_id = fields.Many2one("res.partner", string="Salesman")
    buyer_id = fields.Many2one("res.users", default=lambda self: self.env.user, string="Buyer")
    type_id = fields.Many2one("estate.property.type")
    tags_id = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(copy=False, default=fields.Datetime.today() + (relativedelta(months=3)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='type',
        selection=[('north', 'North'), ('south', 'South'), ('East', 'east'), ('West', 'west')],
    )
    total_area = fields.Integer(string="Total Area", compute="_compute_total_surface")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")

    # ==========constraints===================
    _check_positive_expected_price = models.Constraint("CHECK (expected_price > 0)", "expected price should be bigger than 0")
    _check_positive_selling_price = models.Constraint("CHECK (selling_price > 0)", "expected price should be bigger than 0")

    @api.constrains("selling_price", "expected_price")
    def _check_enough_selling_price(self):
        for record in self:
            offer_made = "accepted" in record.offer_ids.mapped("status")
            price_good_enough = record.selling_price > 0.9 * record.expected_price
            if not price_good_enough and offer_made:
                to_low_user_error = "selling price is too low for the expected price"
                raise exceptions.ValidationError(to_low_user_error)

    @api.constrains("state")
    def _no_sell_without_offer(self):
        for record in self:
            if record.state == "sold" and "accepted" not in record.offer_ids.mapped("status"):
                only_sold_if_accepted = "can only sell a property with an accepted offer"
                raise exceptions.UserError(only_sold_if_accepted)

    # ==========computed fields===============
    @api.depends('garden_area', 'living_area')
    def _compute_total_surface(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            if not record.offer_ids:
                record.best_offer = 0
            else:
                record.best_offer = max(record.offer_ids.mapped("price"))

    # ============onchage fields==============
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # ==========button functions==============
    def action_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                no_sell_cancelled_error = "Can't sell a cancelled property"
                raise exceptions.UserError(no_sell_cancelled_error)
            record.state = "sold"
        return True

    def action_property_cancelled(self):
        for record in self:
            if record.state == "sold":
                no_sell_a_sold_property = "Can't cancel a sold property"
                raise exceptions.UserError(no_sell_a_sold_property)
            record.state = "cancelled"
        return True

    @api.ondelete(at_uninstall=False)
    def ondelete(self):
        for property in self:
            if property.state in ("new", "cancelled"):
                no_delete_new_or_cancelled_record = "cannot delete new or cancelled record"
                raise exceptions.UserError(no_delete_new_or_cancelled_record)
