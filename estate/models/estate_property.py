from odoo import models, fields


class TestModel(models.Model):                              # Inheritence -> This class inherits from models.Model
    _name = "estate_property_model"                         # Name of the table in database
    _description = "Estate Property Model"                  # user-friendly name    

    name = fields.Char(required=True)                       # VARCHAR & NOT NULL
    expected_price = fields.Float(required=True)            # NUMERIC & NOT NULL
    description = fields.Char()