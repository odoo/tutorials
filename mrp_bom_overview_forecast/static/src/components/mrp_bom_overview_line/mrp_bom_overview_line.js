import { patch } from "@web/core/utils/patch";
import { BomOverviewLine } from "@mrp/components/bom_overview_line/mrp_bom_overview_line";

patch(BomOverviewLine.prototype, {
    get ColorClass() {
        switch (this.data.availability_state) {
            case "available":
                return "text-bg-success";
            case "expected":
                return "text-bg-warning";
            case "unavailable":
                return "text-bg-danger";
            default:
                return "text-bg-dark";
        }
    }
});
