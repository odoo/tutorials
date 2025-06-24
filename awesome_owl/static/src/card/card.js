import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "my_module.Card";


    setup() {
        this.state = useState({ isToggled: true });
    }

    static props = {
        title: {type: String},
        slots: {
            type: Object,
            shape: { default:true },
        },
    }

    toggle() {
        this.state.isToggled = !this.state.isToggled;
        if (this.props.onChange) {
            this.props.onChange(this.state.isToggled);
        }
    }

}