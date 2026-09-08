import { Component } from '@odoo/owl';

export class Card extends Component {
    static template = 'awesome_owl.card';
    // static props = {
    //     // title: { type: 'string', default: '<h1>markup in t-esc</h1>' },
    //     content: { type: 'string' },
    // };
    static props = ['title', 'content'];
}
