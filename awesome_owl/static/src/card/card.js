import { Component, useState } from '@odoo/owl';

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: {type: String},
        slots: {
            content: {type: Object}
        }
    }

    setup() {
        this.state = useState({
            toggleStatus: true,
        })
    }

}
