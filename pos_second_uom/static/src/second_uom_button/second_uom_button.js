import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SecondUomPopup } from "@pos_second_uom/second_uom_popup/second_uom_popup";
import { patch } from "@web/core/utils/patch";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { _t } from "@web/core/l10n/translation";

patch(ControlButtons.prototype, {
    displaySecondUomBtn() {
        const selectedLine = this.currentOrder?.getSelectedOrderline();
        return selectedLine && selectedLine.product_id.pos_second_uom_id;
    },

    async clickSecondUom() {
        const selectedLine = this.currentOrder.getSelectedOrderline();
        if (!selectedLine) return;

        const secondUom = selectedLine.product_id.pos_second_uom_id;
        const mainUom = selectedLine.product_id.uom_id;

        const result = await makeAwaitable(this.dialog, SecondUomPopup, {
            title: _t("Secondary Unit Entry"),
            uomName: secondUom.name,
            startingValue: 0,
        });

        if (result !== null && result !== undefined) {
            const enteredQty = parseFloat(result);
            if (isNaN(enteredQty)) return;
            const newMainQty = (enteredQty * secondUom.factor) / mainUom.factor;
            selectedLine.setQuantity(newMainQty);
        }
    }
});
