/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { QuantityDialog } from "../quantity_dialog/quantity_dialog";
import { _t } from "@web/core/l10n/translation";

patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.quantity = '';
        this.handleQuantityConfirm = this.handleQuantityConfirm.bind(this);
    },

    async handleQuantityConfirm(enteredQuantity) {
        const selectedOrder = this.pos.get_order()?.get_selected_orderline();
        const secondUomRecord = selectedOrder.product_id.second_uom_id;
        const factorInv = secondUomRecord?.factor_inv || 1;
        const baseUom = selectedOrder.product_id.uom_id;
        const productPrice = selectedOrder.product_id.lst_price;
        const convertedQuantity = (factorInv === 1)
            ? enteredQuantity * baseUom.factor_inv
            : enteredQuantity / factorInv;
        selectedOrder.set_quantity(convertedQuantity);
        selectedOrder.price_unit = (factorInv === 1)
            ? productPrice / baseUom.factor_inv
            : productPrice * factorInv;
        selectedOrder.set_unit(secondUomRecord);
        selectedOrder.product_id.is_use_second_uom = true;
    },

    onClick() {
        const selectedOrder = this.pos.get_order()?.get_selected_orderline();
        if (!selectedOrder) {
            this.notification.add(_t("No product? No problem! Oh wait... actually, it is a problem. 😅"), {
                type: 'info',
            });
            return;
        }
        if (!selectedOrder.product_id.second_uom_id) {
            this.notification.add(_t("A product without a second unit of measure is like a joke without a punchline. Let fix that! 😄"), {
                type: 'info',
            });
            return;
        }
        this.dialog.add(QuantityDialog, {
            quantity: this.quantity,
            onConfirm: this.handleQuantityConfirm,
        });
    }
});
