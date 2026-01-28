import { Component, useState } from "@odoo/owl";
// import { props } from "@odoo/owl";

export class Card extends Component {
    static template = "my_module.Card";
    static props = {
        title: {
            type: String,
            required: true,
        },
        slots: {
            type: Object,
            optional: true,
        },
    };
    setup() {
        // this.state = {title: this.props.title, content: this.props.content, html: this.props.html};
        this.state = useState({title: this.props.title, visibile: false});
    }
    toggleVisibility() {
        this.state.visibile = !this.state.visibile;
    }

}
