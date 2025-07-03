import { Component } from "@odoo/owl"
import { PieChart } from "../pieChart/piechart"

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem"
    static components = { PieChart }

    static props = {
        size: { type: Number, optional: true, default: 1 },
        slots: {
            type: Object,
            shape: { default: true },
        },
    }
}
