import { patch } from "@web/core/utils/patch";
import { BomOverviewLine } from "@mrp/components/bom_overview_line/mrp_bom_overview_line";

patch(BomOverviewLine.prototype, {

    get statusData() {
        if (this.data.hasOwnProperty('components_available')) {
            const qty = parseInt(this.data.producible_qty) || 0;
            if (qty > 0) {
                return this.data.status;
            }
            if (qty == 0 && this.data.availability_display) {
                return this.data.availability_display;
            }
        }
        if (this.data.availability_display) {
            return this.data.availability_display;
        }

        return "Not Available";
    },

    get statusBackgroundClass() {
        if (this.data.hasOwnProperty('components_available')) {
            const qty = parseInt(this.data.producible_qty) || 0;
            if (qty > 0) {
                return "text-bg-success";
            }
        }

        const state = this.data.availability_state;
        switch (state) {
            case "available":
                return "text-bg-success";
            case "expected":
                return "text-bg-warning";
            case "estimated":
                return "text-bg-dark";
            default:
                return "text-bg-danger";
        }
    },
});
