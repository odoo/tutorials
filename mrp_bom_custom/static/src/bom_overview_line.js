import { patch } from "@web/core/utils/patch";
import { BomOverviewLine } from "@mrp/components/bom_overview_line/mrp_bom_overview_line";

patch(BomOverviewLine.prototype, {
    get statusBackgroundColor() {
        console.log(this.data)
        if (this.data.level !== 0 && this.data.availability_state == 'estimated') {
            return "text-bg-warning";
        }
        switch (this.data.availability_state) {
            case "available": return "text-bg-success";
            case "expected": return "text-bg-warning";
            case "unavailable": return "text-bg-danger";
            default: return "text-bg-dark";
        }
    }
});
