import { patch } from "@web/core/utils/patch";
import { BomOverviewLine } from "@mrp/components/bom_overview_line/mrp_bom_overview_line";

patch(BomOverviewLine.prototype, {

    get statusData() {
        if (this.data.hasOwnProperty('components_available') && this.data.status && this.data.status !== "No Ready To Produce") {
            return this.data.status;
        }
        if (this.data.status === "No Ready To Produce" && this.data.availability_display) {
            return this.data.availability_display;
        }
        if (this.data.availability_display) {
            return this.data.availability_display;
        }

        return "Not Available";
    },

    get statusBackgroundClass() {
        if (!this.statusData) {
            return "text-bg-danger";
        }
        if (this.statusData === "Available" || this.statusData.includes("Ready To Produce")) {
            return "text-bg-success";
        }
        if (this.statusData.includes("Expected")) {
            return "text-bg-warning";
        }
        if (this.statusData.includes("Estimated")) {
            return "text-bg-dark";
        }
        return "text-bg-danger";
    },
});
