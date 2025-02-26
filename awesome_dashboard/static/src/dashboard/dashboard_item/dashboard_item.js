import {Component} from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static defaultProps = {
        size: 1,
    };
    static props = {
        slots: {type: Object, optional: true},
        size: {type: Number, optional: true, default: 1},
        item: {type: Object, optional: true},
    };
}
