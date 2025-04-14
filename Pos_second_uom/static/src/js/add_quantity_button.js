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
        this.product = this.props.product;
        this.orderline = this.props.orderline;
        console.log("ajay");
        this.conversionRatio = 5;
        
    }

    confirm() {
        const qty = this.state.quantity;
        const convertedQty = qty * this.conversionRatio;

        if (this.orderline) {
            this.orderline.set_quantity(convertedQty);
        }

        this.props.close();
    }

    cancel() {
        this.props.close();
    }
}
