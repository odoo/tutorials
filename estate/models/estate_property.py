from odoo import api, models, fields


class EstatePropertyModel(models.Model):                              # Inheritence -> This class inherits from models.Model
    _name = "estate_property_model"                         # Name of the table in database
    _description = "Estate Property Model"                  # user-friendly name    

    name = fields.Char(required=True)                       # VARCHAR & NOT NULL
    expected_price = fields.Float(required=True)            # NUMERIC & NOT NULL
    description = fields.Char()

    living_area = fields.Integer()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")

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