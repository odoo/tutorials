import {Component, markup, useState} from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static defaultProps = {
        collapsable: true,
    }

    static props = {
        title: String,
        description: {type: String, optional: true},
        help: {type: String, optional: true},
        slots: {optional: true},
        collapsable: {optional: true, default: true},
    }

    setup() {
        super.setup();

        this.state = useState({
            title: this.props.title,
            help: this.props.help ? markup(this.props.help) : null,
            collapsed: false,
        });
    }

    toggleCollapse() {
        if (!this.props.collapsable) {
            return;
        }

        this.state.collapsed = !this.state.collapsed;
    }
}
