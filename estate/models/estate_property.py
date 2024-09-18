from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "EstateProperty"
    _order = "id desc"
    # created the field for the estate.property model
    name = fields.Char(required=True, default="Unkown")
    description = fields.Text()
    property_type_id = fields.Many2one("estate.property.type", string="Property Types")
    postcode = fields.Char()
    date_availablity = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default="2")
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_recieved", "Offer Recieved"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        readonly=True,
    )
    active = fields.Boolean(default=True)
    saler_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        index=True,
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total = fields.Integer(compute="_compute_area")
    best_price = fields.Integer(compute="_compute_bestprice")

    # created the sql constraints for only accepting positive values for expected price and selling price
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0.0)",
            "A property expected price must be strictly positive and Grater then Zero.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0.0)",
            "A property selling price must be positive and Grater then Zero.",
        ),
    ]

    # created the area computation function that will compute area from living area and garden area i.e living area + garden area
    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total = record.living_area + record.garden_area

    # created the best price computation function that will compute best price from offers i.e maximum from the offers
    @api.depends("offer_ids")
    def _compute_bestprice(self):
        for record in self:
            if record.offer_ids:
                max1 = 0
                for i in record.offer_ids:
                    if i.price > max1:
                        max1 = i.price
                    record.best_price = max1
            else:
                record.best_price = 0

    # created the garden onchange function that will change the values of the dependent fiels when the particular field triger is activated i.e turning on the garden field will affect the dependent fields
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"

    # created a python constraint that will check weather the selling price is grater then the 90% of the expected price
    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if (
                record.selling_price == 0
                or record.selling_price >= (90 / 100) * record.expected_price
            ):
                pass
            else:
                raise ValidationError(
                    "the selling price cannot be lower than 90'%' of the expected price."
                )

    # creating a delection check function that will check if the property is sold or not
    @api.ondelete(at_uninstall=False)
    def _check_property(self):
        if any(user.state not in ("new", "canceled") for user in self):
            raise UserError("You can't delete a property that is in process.")

    # created the action for the sold button that will chage the state field of the property to sold
    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError(
                    "This Property couldn't be sold Because it is alredy canceled."
                )
            elif record.state == "sold":
                raise UserError("This property is alredy Sold.")
            else:
                record.state = "sold"
        return True

    # created the action for the cancel button that will change the state of the property to canceled
    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("This property is alredy sold. You can't cancel it.")
            elif record.state == "canceled":
                raise UserError("This property is alredy canceled.")
            else:
                record.state = "canceled"
        return True
