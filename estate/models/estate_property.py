from odoo import fields, models
from odoo.tools import date_utils

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property for purchasing and selling properties"
    
    # _log_access = False # this will disable the automatic creation of create_uid,create_date,write_uid,write_date fields in our table. these fields are used to track who created and modified the record and when it was done.
    title = fields.Char(required=True) 
    description = fields.Char()
    postcode = fields.Char()
    date_availibility = fields.Date(copy=False,  default=lambda self: fields.Date.today() + date_utils.get_timedelta(3, "month"))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),  # value,label
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),

        ],
    )
    status = fields.Selection(
        selection = [
            ('new','New'),
            ('offer received','Offer received'), 
            ('offer accepted','Offer accepted'),
            ('sold','Sold'), 
            ('cancelled','Cancelled')
        ],
    )   
    active = fields.Boolean()

    # module: a module is a package of features/functionality in odoo.Ex : CRM,Sales,EstateProperty.it's a complete feature bundle
    # model : model is a python class that define data structure and logic.it represent a real world entity
    # table: a table is the actual data stored in database.our _name = "estate.property" will converted to estate_property table name
    # relationship : module -> model -> table

    # Odoo's ORM calls `_auto_init()` on your model, which introspects all fields and runs `CREATE TABLE` / `ALTER TABLE`. Here's roughly what happens:
    # ```
    # _name = "estate.property" => estate is a module name and property is a model name this tells that "property" belongs to estate module. giving name like using dot (estate.property) is a odoo convention
    # table name = "estate_property"
    # The _ prefix tells Odoo "this is configuration about the model itself", not "this is a field to store in the database".


    #what is happening in backend? how odoo is connecting to psql even if we are not adding code to connect it?
    #=>when odoo load's our model it convert out table name estate.property to estate_property
    #=> Odoo's base Model class (which your class inherits from) has a method called _auto_init(). This runs automatically during module install/upgrade.
    #=> inside auto_init method there is self._cr, it's a database cursor this is the actual live connection to postgresql.it send the connection request to psycopg2 py library and this library establish the connection to psql

