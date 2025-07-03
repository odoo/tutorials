/** @odoo-module **/

import { Component, useRef } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class AddQuantityDialog extends Component {
    static template = "pos_second_uom.AddQuantityDialog";

    static components = { Dialog };

    static props = {
        close: { type: Function }
    };

    setup() {
        this.pos = usePos()
        this.quantityInputRef = useRef("quantityInput");
    }

    confirm() {
        const quantity = this.quantityInputRef.el.value;
        const order = this.pos.get_order();
        const selectedOrderline = order.get_selected_orderline();
        const product = selectedOrderline.get_product();
        const originalUOM = product.uom_id.category_id.uom_ids[0];
        const secondUOM = product.uom_id.category_id.uom_ids[1];
        const convertedQuantity = quantity * (secondUOM.factor_inv / originalUOM.factor);
        selectedOrderline.set_quantity(convertedQuantity);
        this.props.close();
    }

    cancel() {
        this.props.close();
    }
}
