import {Component} from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";

    static props = {
        value: {type: Number},
        onChange: {type: Function},
    };
}
