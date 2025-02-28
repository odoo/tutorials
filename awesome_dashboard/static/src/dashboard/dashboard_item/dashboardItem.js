import { Component, useState } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.item";

    static props = {
        title: { type : String, optional : true },
        slots: { type : Object },
        size: { type : Number, optional : true },
        toggle: { type : Boolean, optional : true },
    }

    static defaultProps = {
        size: 1,
        toggle: false,
    };

    setup(){
        this.state = useState({
            toggled : this.props.toggle,
        })
    }

    toggle(){
        this.state.toggled = !this.state.toggled;
    }
}