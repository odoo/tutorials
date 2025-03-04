from odoo import fields, models


class ResUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        string="Properties",
        help="Properties sold by the user.",
        comodel_name="estate.property",
        inverse_name="salesperson_id",
        domain=['|',('state','=','new'),('state','=','offer_received')],
    )
