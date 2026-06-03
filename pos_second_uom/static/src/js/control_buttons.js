import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { NumberPopup } from "@point_of_sale/app/components/popups/number_popup/number_popup";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons.prototype, {
    displaySecondUomButton() {
        const line = this.currentOrder?.getSelectedOrderline();
        return line?.product_id?.pos_second_uom_id;
    },

    async clickSecondUomButton() {
        const line = this.currentOrder?.getSelectedOrderline();

        if (!line) {
            return;
        }

        const secondUom = line.product_id.pos_second_uom_id;
        const mainUom = line.product_id.uom_id;

        const qty = await makeAwaitable(
            this.dialog,
            NumberPopup,
            {
                title: `Enter ${secondUom.name} Quantity`,
                startingValue: 0,
            }
        );

        if (qty === null || qty === undefined) {
            return;
        }

        const enteredQty = parseFloat(qty);

        if (isNaN(enteredQty)) {
            return;
        }

        const convertedQty = (enteredQty * secondUom.factor) / mainUom.factor;

        line.setQuantity(convertedQty);
    },
});
