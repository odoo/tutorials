import { patch } from "@web/core/utils/patch";
import { BomOverviewLine } from "@mrp/components/bom_overview_line/mrp_bom_overview_line";


patch(BomOverviewLine.prototype, {
    get status() {
        let ready_to_produce = this.data.producible_qty ? this.data.producible_qty > 0 : false;

        if (this.data.hasOwnProperty('components_available') && this.data.status && ready_to_produce) {
            return this.data.status;
        }
        if (!ready_to_produce && this.data.availability_display) {
            return this.data.availability_display;
        }
        if (this.data.availability_display) {
            return this.data.availability_display;
        }

        return "Not Available";
    },
    get statusStyleClass() {
        let ready_to_produce = this.data.producible_qty ? this.data.producible_qty > 0 : false;

        if (!this.status || this.status == "Not Available") return "text-bg-danger";
        if (this.status && (ready_to_produce || this.status === "Available")) {
            return "bg-success text-white fw-bold";
        }
        if (this.status && this.status.includes("Estimated")) return "text-bg-warning";
        if (this.status && !ready_to_produce) {
            return "bg-dark text-white fw-bold";
        }
        return "text-bg-danger";
    }
})
