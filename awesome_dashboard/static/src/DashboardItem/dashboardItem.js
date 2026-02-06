import { Component } from "@odoo/owl";


export class DashboardItem extends Component {
    static template = "dashborad.dashboardItem";
    static props = {
        size: { type: Number, optional: true, default: 1 },
        slots: { type: Object, optional: true },
    };
}
