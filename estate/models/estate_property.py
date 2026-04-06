from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property for purchasing and selling properties"

    name = fields.Char(required=True)
    description = fields.Char()
    postcode = fields.Char()
    date_availibility = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
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