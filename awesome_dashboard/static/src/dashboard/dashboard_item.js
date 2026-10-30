import { Component, t, useProps } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";

    props = useProps({
        size: t.number().optional(1)
    });
}