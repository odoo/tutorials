from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type like House, Apartment, Penthouse"

    #---------------------------------------------------------------------
    # Fields
    #---------------------------------------------------------------------
    name = fields.Char(required=True)


    #---------------------------------------------------------------------
    # Relations
    #---------------------------------------------------------------------
    property_ids = fields.One2many("estate.property.type.line", "model_id", string="Property Id")
    


class EstatePropertyTypeLine(models.Model):
    _name = "estate.property.type.line"
    _description = "This is a inline model of Property Type"

    model_id = fields.Many2one("estate.property.type")
    title = fields.Char()
    expected_price = fields.Float()
    status = fields.Char()

