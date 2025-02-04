import { Component, useState } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem"
    static props = {
        size: { type: Number, optional: true, default: 1 },
        className: { type: String, optional: true, default: "" },
    };
}