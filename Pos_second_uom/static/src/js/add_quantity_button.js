/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/store/pos_hook";


export class SecondaryUomDialog extends Component {
    static template = "pos_secondary_uom.SecondaryUomDialog";
    static components = { Dialog };

    setup() {
        this.pos = usePos();
        this.state = useState({ quantity: 1 });

        this.orderline = this.props.orderline;
        console.log(this.orderline);
        const uomIds = this.orderline.product_id.uom_id.category_id.uom_ids;

        this.baseUom = uomIds[0];
        this.secondaryUom = uomIds[1];
        this.conversionRatio = 1;
        if (this.secondaryUom && this.baseUom) {
            const secondaryFactor = this.secondaryUom.factor;
            const baseFactor = this.baseUom.factor;
            this.conversionRatio = baseFactor / secondaryFactor;
        }
    }

    confirm() {
        const enteredQty = parseFloat(this.state.quantity);
        if (isNaN(enteredQty) || enteredQty <= 0) {
            this.pos.env.services.notification.add("Enter a valid quantity", { type: "warning" });
            return;
        }

        const baseQty = enteredQty * this.conversionRatio;
        this.orderline.set_quantity(baseQty);
        this.orderline.uom_id = this.secondaryUom;
        this.props.close();
    }

    cancel() {
        this.props.close();
    }
}
