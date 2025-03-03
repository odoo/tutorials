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

    setup() {
        this.orm = this.env.services.orm;
        this.pos = usePos();

        this.state = useState({
            quantity: 1,
            secUomId: null,
            secUoms: [],
        });

        this.productId = this.props.productId;
        this.uomId = this.props.uomId;

        onWillStart(async () => {
            const productData = await this.orm.searchRead(
                "product.template",
                [["id", "=", this.productId]],
                ["sec_uom_id"]
            );

            if (!productData.length || !productData[0].sec_uom_id) return;

            const secUomId = productData[0].sec_uom_id[0];

            const uomsData = await this.orm.searchRead(
                "uom.uom",
                [["id", "in", [secUomId, this.uomId]]],
                ["id", "name", "category_id"]
            );

            const secUom = uomsData.find((uom) => uom.id === secUomId);
            if (!secUom) return;

            const categoryId = secUom.category_id[0];

            this.state.secUoms = uomsData.filter(
                (uom) => uom.category_id[0] === categoryId && uom.id !== this.uomId
            );

            this.state.secUomId = this.state.secUoms.length ? this.state.secUoms[0].id : null;
        });
    }

    async confirmSelection() {
        const uomsData = await this.orm.searchRead(
            "uom.uom",
            [["id", "in", [this.state.secUomId, this.uomId]]],
            ["id", "factor", "uom_type"]
        );

        const secUomData = uomsData.find((uom) => uom.id === this.state.secUomId);
        const firstUomData = uomsData.find((uom) => uom.id === this.uomId);

        if (!firstUomData || !secUomData) {
            console.log("UOM data missing, cannot confirm selection.");
            return;
        }

        this.props.onConfirm(
            this.state.quantity,
            firstUomData.uom_type,
            secUomData.factor,
            firstUomData.factor,
            secUomData.uom_type
        );
        this.props.close();
    }

    cancel() {
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

        this.productId = selectedOrder.product_id._raw.product_tmpl_id;
        this.uomId = selectedOrder.product_id.uom_id.id;

        // Fetch product and UOM data in a single query
        const productData = await this.orm.searchRead(
            "product.template",
            [["id", "=", this.productId]],
            ["sec_uom_id"]
        );

        this.showCustomButton.value = productData.length > 0 && productData[0].sec_uom_id;
    },

    // Open the ConfigurationDialog
    openConfigurationDialog() {
        this.dialog.add(ConfigurationDialog, {
            uomId: this.uomId,
            productId: this.productId,
            onConfirm: (quantity, uomType, secFactor, factor, secUomType) =>
                this.handleDialogConfirm(quantity, uomType, secFactor, factor, secUomType),
        });
    },

    // Apply selected UOM conversion to order line quantity
    handleDialogConfirm(quantity, uomType, secFactor, factor, secUomType) {
        const orderline = this.pos.get_order().get_selected_orderline();
        if (!orderline) return;

        if (secUomType === "bigger") {
            orderline.set_quantity(quantity * secFactor);
        } else {
            orderline.set_quantity(
                uomType === "bigger" ? quantity * factor : quantity / secFactor
            );
        }
    },
});
