import { Component } from '@odoo/owl';

export class NumberCard extends Component {
    static template = "awesome_owl.number_card";
    static props = {
        value: {
            type: Number,
        },
        title: {
            type: String,
        },
    };
}
