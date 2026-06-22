from odoo import api, models, fields, exceptions


class EstatePropertyModel(models.Model):                    # Inheritence -> This class inherits from models.Model
    _name = "estate_property_model"                         # Name of the table in database
    _description = "Estate Property Model"                  # user-friendly name    
    _order = "id desc"

    name = fields.Char(required=True)                       # VARCHAR & NOT NULL
    expected_price = fields.Float(required=True)            # NUMERIC & NOT NULL
    description = fields.Char()

    living_area = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([("north", 'North'), ('south', 'South'), ('east', "East"), ("west", 'West')])
    total_area = fields.Integer(compute="_compute_total_area")

    best_price = fields.Float(compute="_compute_best_offer_price", string="Best Accepted Offer")

    sold = fields.Boolean()
    cancelled = fields.Boolean()
    property_status = fields.Char(default="New", string="Property Status")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    property_type_id = fields.Many2one(
        comodel_name="estate_property_type_model",
        string="Property Type",
        ondelete="set null"
    )
    property_tag_ids = fields.Many2many(
        comodel_name="estate_property_tag_model",
        relation="estate_property_tag_rel",
        column1="estate_property_id",
        column2="estate_property_tag_id",
        string="Tag"
    )
    property_offer_ids = fields.One2many(
        comodel_name="estate_property_offer_model", 
        inverse_name="property_id", 
        string="Property Offers"
    )

    @api.depends("property_offer_ids")
    def _compute_best_offer_price(self):
        for record in self:
            accepted_offers= record.property_offer_ids.filtered(lambda rec: rec.status == "accepted")
            prices = accepted_offers.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_property_sold(self):
        if(self.cancelled==False):
            self.sold = True
            self.property_status = "Sold"
            return True
        else:
            raise exceptions.UserError("Cancelled properties can't be sold")

    def action_property_cancelled(self):
        if (self.sold==False):
            self.cancelled = True
            self.property_status = "Cancelled"
            return True
        else:
            raise exceptions.UserError("Sold properties can't be cancelled")
        
    @api.constrains("expected_price")
    def _check_expected_price_positive(self):
        for record in self:
            if(record.expected_price<=0):
                raise exceptions.ValidationError("The price must be a positive number")