/** @odoo-module **/

import {Component, markup, useState} from "@odoo/owl"
import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import {List} from "./to_do_list/to_do_list"
export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter,Card, List};
    setup(){
        this.count=useState({value:0});
        this.cnt1 = "<b>content1</b>";
        this.cnt2 = markup("<i>content2</i>");
    }
    incre(){
        this.count.value++;
    }
}
