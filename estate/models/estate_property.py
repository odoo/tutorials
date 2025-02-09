from odoo import models, fields

class estateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property"
    

    name= fields.Char("Property Name", required = True) # required make property not nullable 
    description =  fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(copy = False, default = lambda self: fields.Date.add(fields.Date.today(), months = 3))  # lambda function delays the execution of this until the record is created
    expected_price = fields.Float("Expected Price", required = True)
    selling_price = fields.Float("Selling Price", readonly = True, copy = False)
    bedrooms = fields.Integer("Bedrooms", default = "2")
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string = "Orientations", selection = [("north", "North"), ("east","East"), ("west","West"), ("south","South")], help = "this is used to select orientations of garden")
    active = fields.Boolean("Active", default = True)
    state = fields.Selection(required = True, copy = False, default = "new", selection = [("new", "New"), ("offer received", "Offer Received"), ("offer accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")])

    property_type_id = fields.Many2one("estate.property.type")
    
    buyer_id = fields.Many2one("res.partner", string = "Buyer", copy = False)  # a buyer is a external person - therefore in partner relation 
    salesperson_id = fields.Many2one("res.users", string = "Salesman", default = lambda self: self.env.user) # a salesman is considered a internal entity - therefore in user relation
    
    tag_ids = fields.Many2many("estate.property.tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string = "Offers")
