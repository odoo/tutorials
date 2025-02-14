from odoo import models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_estate_property_sold(self):
        print("=================== Sold button clicked from account application")
        # for record in self:
        #     if (
        #         record.status == "new"
        #         or record.status == "offer_accept"
        #         or record.status == "offer_receive"
        #     ):
        #         record.status = "sold"
        #     elif record.status == "cancelled":
        #         raise UserError("Cancelled property can't be sold")
        #     else:
        #         raise UserError("Property already sold")

        return super().action_estate_property_sold()
