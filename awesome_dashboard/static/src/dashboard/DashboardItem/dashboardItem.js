import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";


export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: {
            type: Number,
            optional: true,
        },
    };
    static defaultProps = {
        size : 1,
    };

    get widthStyle() {
        return `width:${18 * this.props.size}rem;`;
    }
}

registry.category("components").add("DashboardItem", DashboardItem);
