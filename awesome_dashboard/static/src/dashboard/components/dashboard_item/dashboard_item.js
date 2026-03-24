import {Component} from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";

    static defaultProps = {
        size: 1,
    }

    static props = {
        size: {type: Number, optional: true},
        slots: {optional: true},
    }

    get size() {
        if (this.env.isSmall) {
            return '100%';
        }

        return `${this.props.size * 18}rem`;
    }
}