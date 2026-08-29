import { Component, useState } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item";
    static props = {
        title: {type: String, optional: true},
        slots: {type: Object, optional: true},
        size: {type: Number, optional: true}
    };
    static defaultProps = {
        title: "",
        size: 1
    }

    setup() {
        this.open = useState({ value: true });
    }
    
    toggleOpen() {
        this.open.value = !this.open.value
    }

    get widthSize() {
        return `${18*this.props.size}rem;`
    }
}
