import {Component} from "@odoo/owl";
import { markup } from "owl";


class Card extends Component {
    static template = "awesome_owl.Card";

    setup() {
       this.title = this.props.title;
       this.content = markup(this.props.content);
    }
}

export {Card}
