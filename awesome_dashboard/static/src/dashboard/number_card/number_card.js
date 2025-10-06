import {Component} from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static defaultProps = {
        size: 1,
    };
    static props = {
        title: {type: String, optional: true},
        value: {type: Number, optional: true},
    };
}
