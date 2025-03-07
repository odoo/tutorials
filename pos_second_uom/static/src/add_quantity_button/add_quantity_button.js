/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Dialog } from "@web/core/dialog/dialog";

import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { usePos } from "@point_of_sale/app/store/pos_hook";

import { Component, onWillStart, useState, useEffect } from "@odoo/owl";

// ConfigurationDialog Component
class ConfigurationDialog extends Component {
    static template = "pos_second_uom.ConfigurationDialog";
    static components = { Dialog };
    static props = { secUomName: String, onConfirm: Function, close: Function };
    
    setup() {
        this.orm = this.env.services.orm;
        this.pos = usePos();

        this.state = useState({
            quantity: 1,
        });
        this.secUomName = this.props.secUomName
    }

    async confirmSelection() {
        this.props.onConfirm(
            this.state.quantity,
        );
        this.props.close();
    }
}

// Patch ControlButtons to integrate the ConfigurationDialog
patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        this.orm = this.env.services.orm;
        this.dialog = this.env.services.dialog;
        this.showCustomButton = useState({ value: false });

        // Monitor selected order line and update state
        useEffect(() => {
            this.getProductDetailsFromOrderLine();
        }, () => [this.pos.get_order().get_selected_orderline()?.id]);
    },

    // Retrieve product and UOM details from the selected order line
    async getProductDetailsFromOrderLine() {
        const order = this.pos.get_order();
        if (!order || order.lines.length === 0) return;

        const selectedOrder = order.get_selected_orderline();
        if (!selectedOrder) return;
        
        this.secUomId = selectedOrder.product_id.sec_uom_id.id;
        this.secUomName = selectedOrder.product_id.sec_uom_id.name;
        this.uomFactor = selectedOrder.product_id.sec_uom_id.factor;
        this.secUomFactor = selectedOrder.product_id.sec_uom_id.factor_inv;
        this.uomType = selectedOrder.product_id.uom_id.uom_type;

        this.showCustomButton.value = this.secUomId
    },

    // Open the ConfigurationDialog
    openConfigurationDialog() {
        this.dialog.add(ConfigurationDialog, {
            secUomName: this.secUomName,
            onConfirm: (quantity) =>
                this.handleDialogConfirm(quantity),
        });
    },

    // Apply selected UOM conversion to order line quantity
    handleDialogConfirm(quantity) {
        const orderline = this.pos.get_order().get_selected_orderline();
        if (!orderline) return;
        if (this.uomType === "bigger") {
            orderline.set_quantity(quantity / this.secUomFactor);
        } else {
            orderline.set_quantity(quantity * this.secUomFactor);
        }
    },
});
