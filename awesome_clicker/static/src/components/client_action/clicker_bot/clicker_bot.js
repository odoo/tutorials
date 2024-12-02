import {Component} from "@odoo/owl";
import {useClick} from "../../../clicker/clicker";
import {ClickValue} from "../../click_value/click_value";

export class ClickerBot extends Component {
    static template = "awesome_clicker.client_action.clicker_bot";

    static props = {
        bot: {
            type: Object
        },
    }

    static components = {ClickValue}

    get iconClass() {
        const res = {
            'fa': true,
            'fa-2x': true
        }
        res[this.props.bot.spec.icon] = true
        return res
    }

    setup() {
        this.clicker = useClick();
    }
}