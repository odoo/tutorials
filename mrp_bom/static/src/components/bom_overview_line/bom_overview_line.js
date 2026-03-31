/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverviewLine } from "@mrp/components/bom_overview_line/mrp_bom_overview_line";

patch(BomOverviewLine.prototype, {
  get statusBackgroundClass() {
    if (this.data.level === 0 && this.data.producible_qty > 0) {
      return "text-bg-success";
    }

    if (this.data.level === 0 && this.data.producible_qty <= 0) {
      return "text-bg-dark";
    }

    switch (this.data.availability_state) {
      case "available":
        return "text-bg-success";
      case "expected":
        return "text-bg-warning";
      case "estimated":
        return "text-bg-secondary";
      case "unavailable":
        return "text-bg-danger";
    }
  },
});
