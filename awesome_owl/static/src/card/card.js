import {useState, Component} from "@odoo/owl"


export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: String,
        slots: Object,
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
        console.log(this.isOpened);
        this.state.isOpened = !this.isOpened;
    }
}
