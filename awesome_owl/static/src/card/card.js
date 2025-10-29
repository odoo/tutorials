import {Component, useState} from "@odoo/owl"


export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: String,
        slots: {type: Object, optional: true},
    };

    setup() {
        const {title} = this.props;
        this.title = title;
        this.state = useState({isOpened: true})
    }

    get isOpened() {
        return this.state.isOpened;
    }

    toggle() {
        this.state.isOpened = !this.isOpened;
    }
}
