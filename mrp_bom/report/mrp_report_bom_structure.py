from odoo import _, models
import math


class MrpBom(models.AbstractModel):
    _inherit = "report.mrp.report_bom_structure"

    def _get_bom_data(self, *args, **kwargs):
        result = super()._get_bom_data(*args, **kwargs)
        self._modify_bom_result(result)
        return result

    def _modify_bom_result(self, data):
        if data.get("producible_qty") is not None:
            qty = math.floor(data["producible_qty"])
            data["producible_qty"] = qty

            if data.get("level") == 0 and qty > 0:
                data["status"] = _("%(qty)s Ready To Produce", qty=qty)

        for component in data.get("components", []):
            if component.get("is_storable"):
                component["status"] = component.get("availability_display")

            if component.get("components"):
                self._modify_bom_result(component)
