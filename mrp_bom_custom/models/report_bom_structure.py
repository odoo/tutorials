from odoo import _, models


class ReportMrpReportBomStructure(models.AbstractModel):
    _inherit = "report.mrp.report_bom_structure"

    def _get_bom_data(self, *args, **kwargs):
        result = super()._get_bom_data(*args, **kwargs)

        if result.get("level") == 0:
            qty = int(result.get("producible_qty") or 0)
            if qty > 0:
                result["status"] = _("%(qty)s Ready To Produce", qty=qty)
            else:
                result["status"] = _("No Ready To Produce")

        return result
