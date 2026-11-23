import { Component, useProps, types as t } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";

    props = useProps({
        size: t.number().optional(1),
    });
}
