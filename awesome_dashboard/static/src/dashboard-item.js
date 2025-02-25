import { Component } from "@odoo/owl"

export class DashboardItem extends Component{
    static template = "awesome_dashboard.DashboardItem"
    // static defaultProps = {
    //     size: 1
    // };
    static props = {
        slots: {
            type: Object,
            shape:{
                default: Object
            }
        },
        size: {
            type: Number,
            optional: true
        },
    };
}