import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboardItem";
    
    static props = {
        id: {type: Number},
        description: {type: String},
        Component: {type: Object},
        size: {type: Number, optional: true},
        props: {type: Function, optional: true}
    }
    static defaultProps = {
        size: 1,
    }

    

}