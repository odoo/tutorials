import { Component } from "@odoo/owl";

export class AwesomeDashboardItem extends Component {
    static template = "awesome_dashboard.AwesomeDashboardItem";
    static props = { 
        size: {
        type: Number,
        optional: true,
        },
        slots : {type: Object, optional: true},
    };
    static defaultProps = {
        size: 1,
      };


}