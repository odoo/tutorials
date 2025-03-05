from odoo import models, fields
from datetime import date

class EstateProperty(models.Model):
    _name = "estate.property" 
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", default=lambda self: date.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()

    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )


# id                 | integer                     |           | not null | nextval('estate_property_id_seq'::regclass)
# create_uid         | integer                     |           |          |
# create_date        | timestamp without time zone |           |          |
# write_uid          | integer                     |           |          |
# write_date         | timestamp without time zone |           |          |
# name               | character varying           |           |          |
# description        | text                        |           |          |
# postcode           | character varying           |           |          |
# date_availability  | date                        |           |          |
# expected_price     | double precision            |           |          |
# selling_price      | double precision            |           |          |
# bedrooms           | integer                     |           |          |
# living_area        | integer                     |           |          |
# facades            | integer                     |           |          |
# garage             | boolean                     |           |          |
# garden             | boolean                     |           |          |
# garden_area        | integer                     |           |          |
# garden_orientation | character varying           |           |          |
# Indexes:
#     "estate_property_pkey" PRIMARY KEY, btree (id)
# Foreign-key constraints:
#     "estate_property_create_uid_fkey" FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL
#     "estate_property_write_uid_fkey" FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL