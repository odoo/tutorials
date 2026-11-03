import { humanNumber } from "@web/core/utils/numbers";
import { Component} from "@odoo/owl";
import { useClicker } from "../clicker_hook/clicker_hook";

export class ClickValue extends Component {
    static template = "awesome_clicker.click_value";
    static components = { };
    static props = [];
    
    setup()
    {
        this.clicker = useClicker();
    }
    get humanClicks(){
        return humanNumber(this.clicker.clicks, {decimals: 1,})
    }
    
}
