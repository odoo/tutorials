import { patch } from "@web/core/utils/patch";
import { BomOverviewLine } from "@mrp/components/bom_overview_line/mrp_bom_overview_line";

patch(BomOverviewLine.prototype, {

    get statusBackgroundColor() {
        switch (this.data.availability_state) {
            case "available": return "text-bg-success";
            case "expected":
            case "estimated":
                if (this.data.level === 0) return "text-bg-dark";
                return "border border-warning text-warning";
            case "unavailable": return "text-bg-danger";
            default: return "text-bg-dark";
        }
    },

    get statusDisplay() {
        if (this.data.level > 0 &&
            this.data.availability_display &&
            this.data.availability_display.includes("Estimated")) {
            return this.data.availability_display.replace(
                "Estimated", "Expected"
            );
        }
        return this.data.availability_display;
    }
});
