import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = 'card.card';
    static props = {
        size: {type: 'Number', optional: 'true',},
        slots: {type: 'Object', optional: 'true',},
        debug: {type: 'Function', optional: 'true',},
    }

    setup() {
        this.size = this.props.size ? this.props.size : 1;
        if (this.props.debug) { this.props.debug(this); }
    }
}
