/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import {
    QtyAtDateWidget,
    qtyAtDateWidget
} from "@sale_stock/widgets/qty_at_date_widget";

/**
 * Patch the QtyAtDateWidget to support warehouse-wise quantity data
 */
patch(QtyAtDateWidget.prototype, {
    /**
     * Update calculation data with warehouse-wise quantities when available
     * @override
     */
    updateCalcData() {
        const { data } = this.props.record;

        // Check if required data is available
        if (!data.product_id || (!data.on_hand_qty_warehouse_wise && !data.forecast_qty_warehouse_wise)) {
            return super.updateCalcData();
        }

        if (!data.on_hand_qty_warehouse_wise) {
            return;
        } else if (!data.forecast_qty_warehouse_wise) {
            return;
        }

        // Set values from warehouse-wise data
        this.calcData.available_qty = data.on_hand_qty_warehouse_wise || {};
        this.calcData.forecast_qty = data.forecast_qty_warehouse_wise || {};

        super.updateCalcData();
    },
});

/**
 * Extended stock widget with additional field dependencies
 */

patch(qtyAtDateWidget, {
    fieldDependencies: [
        { name: "on_hand_qty_warehouse_wise", type: "object" },
        { name: "forecast_qty_warehouse_wise", type: "object" },
    ],
})
