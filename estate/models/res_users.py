from odoo import api,fields,models

class res_users(models.Model):
    # Private attributes
    _inherit = "res.users"

    # Fields declaration
    property_ids = fields.One2many("estate.property","property_salesman_id",string="Properties",domain=[("estate_state","in",["New","Offer_Received"])])

    # @api.onchange("property_ids")
    # def _onchange_garden(self):
    #     print("####################################################")
    #     for record in self:
    #         print(record.property_ids)