import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";
import { useService } from "@web/core/utils/hooks";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        data: Object,
    };

    setup() {
        this.action = useService("action");
    }

    onSliceClick(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: `Orders - Size ${size.toUpperCase()}`,
            res_model: "sale.order",
            views: [[false, "list"], [false, "form"]],
            domain: [["order_line.product_id.name", "ilike", size]],
        });
    }
}
