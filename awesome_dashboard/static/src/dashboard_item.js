
import { Component } from "@odoo/owl";


export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item";
    static props = {
        slots: Object,
        size: {
            type: Number,
            optional: true
        }
    };


    calculate_width(){
        if (this.props.size){
            this.width = (18*this.props.size)
        }else{
            this.width = 18
        }
        return this.width
    }
}
