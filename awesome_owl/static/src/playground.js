/** @odoo-module **/

import { Component, useState ,markup} from "@odoo/owl";

import { Counter } from "./Counter/counter";
import { Card } from "./Card/card";
export class Playground extends Component {
    static template = "awesome_owl.playground";
    // state = useState({ value: 0 });

    static components={Counter,Card};
    setup(){
        this.state=useState({sum:2});
    }
    
    increment_sum(){
        this.state.sum+=1;
    }


}

