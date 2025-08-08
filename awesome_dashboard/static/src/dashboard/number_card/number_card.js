import { Component } from "@odoo/owl";
import { Card } from "../card/card";


export class NumberCard extends Component {
    static template = 'number_card.number_card';
    static components = { Card };
    static props = {
        title: {type: 'String', optional: 'true',},
        value: {type: 'Number', optional: 'true',},
        size: {type: 'Number', optional: 'true',},
        stringProps: {type: 'String', optional: 'true',},

    }
    setup() {
        if (this.props.stringProps) {
            this.stringProps = JSON.parse(this.props.stringProps);
            this.title = this.stringProps.title ? this.stringProps.title : 'No Title.';
            this.value = this.stringProps.value ? this.stringProps.value : 0;
            this.size = this.stringProps.size;
        } else {
            this.title = this.props.title ? this.props.title : 'No Title.';
            this.value = this.props.value ? this.props.value : 0;
            this.size = this.props.size;
        }
    }
}
