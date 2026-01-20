from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
      result = super().session_info()
      user = request.env.user
      result["is_company"] = user.partner_id.is_company
      return result
