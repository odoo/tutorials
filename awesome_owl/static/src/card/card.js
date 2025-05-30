import {Component, markup, useState} from "@odoo/owl";


export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {title: {type: String}, slots: {type: Object}};

    html_jojo_joke = "<p>Jojo be like muda muda muda muda (less funny when you write it)</p>";
    html_markup_jojo_joke = markup("<p>Jojo be like muda muda muda muda (less funny when you write it)</p>");

    state = useState({isOpened: true});

    toggleVisibility() {
        this.state.isOpened = !this.state.isOpened;
    }
}
