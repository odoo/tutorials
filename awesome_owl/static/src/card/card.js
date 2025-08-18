import { Component, useState } from '@odoo/owl';

export class Card extends Component {
    static template = 'awesome_owl.Card';
    static props = {
        title: {
            type: String,
            optional: false,
        },
        slots: {
            type: Object,
            optional: true,
        }
    }

    setup() {
        this.isBodyOpen = useState({
            value: true,
        });    
        this.toggleBodyOpen = this.toggleBodyOpen.bind(this);
    }

    toggleBodyOpen() {
        this.isBodyOpen.value = !this.isBodyOpen.value;
    }
}