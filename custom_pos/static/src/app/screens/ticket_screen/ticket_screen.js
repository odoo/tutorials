import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";


patch(TicketScreen.prototype, {
    _getSearchFields() {
        const fields = super._getSearchFields()
        fields.BARCODE = {
            repr: (order) => order?.lines?.map(line => line?.product_id?.barcode || "").filter(barcode => barcode),
            displayName: _t("Product Barcode"),
            modelField: "lines.product_id.barcode",
        };
        return fields;
    },
});
