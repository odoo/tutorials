import {Component} from "@odoo/owl"
import {NumberCard} from "../number_card/number_card";


export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item";
    static props = {
        size: {type: Number, optional: true, default: 1},
        slots: {type: Object, optional: true, default: null},
    };
    static components = {NumberCard};
}
