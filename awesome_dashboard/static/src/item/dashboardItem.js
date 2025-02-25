import { Component, useState } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.item";

    static props = {
        title: { type : String },
        slots: { type : Object },
        size: { type : Number, optional : true },
    }

    static defaultProps = {
        size: 1,
    };
    

    setup(){
        this.state = useState({
            toggled : false,
        })
    }

    toggle(){
        this.state.toggled = !this.state.toggled;
    }
}