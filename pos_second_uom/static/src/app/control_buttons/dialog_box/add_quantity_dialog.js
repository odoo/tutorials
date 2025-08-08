/** @odoo-module **/

import { Component, useRef } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";

export class AddQuantityDialog extends Component {
    static template = "pos_second_uom.AddQuantityDialog";
    static components = { Dialog };
    static props = {
        close: { type: Function },
        product: { type: Object },
        orderline: { type: Object },
        secondUomName: { type: String, optional: true },
    };

    setup() {
        this.pos = usePos();
        this.input_qty = useRef("quantityInput");
        this.uom_ratio = this.computeUomRatio(this.props.product);
        this.dialog = useService("dialog");
    }

    computeUomRatio(product) {
        if (product.uom_id && product.pos_second_uom_id) {
            return product.uom_id.factor / product.pos_second_uom_id.factor;
        }
        return 1;
    }

    confirm() {
        const quantity = parseFloat(this.input_qty.el.value);
        if (!quantity || quantity <= 0) {
            this.pos.dialog.add(AlertDialog, {
                title: _t("Error"),
                body: _t("Oops!!!!! Quantity cannot be negative, zero, or empty. Please enter a valid positive number !!"),
            });
            return;
        }
        this.props.orderline.set_quantity(quantity * this.uom_ratio);
        this.props.close();
    }
}
