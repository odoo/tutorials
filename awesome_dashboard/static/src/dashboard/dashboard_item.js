import { Component } from "@odoo/owl";
import { Layout } from "@web/search/layout";

export class AwesomeDashboardItem extends Component {
    static components = { Layout };
    static template = "awesome_dashboard.AwesomeDashboardItem";

    static defaultProps = {
        size: 1,
    };

    static props = {
        size: { type: Number, optional: true },
        slots: {
            type: Object,
            shape: {
                default: true,
            },
        },
    };
}
