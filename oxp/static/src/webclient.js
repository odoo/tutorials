/** @odoo-module **/
import {Component} from "@odoo/owl";
import {Navbar} from "./navbar/navbar";
import {Todoo} from "./todoo/todoo";


export class WebClient extends Component {
    static template = "oxp.home";
    static components = { Navbar, Todoo};
    static props = {};


}
