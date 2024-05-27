/** @odoo-module **/

import {Component, useState, useRef, onMounted} from "@odoo/owl";
import {Item} from "./to_do_item";

export class List extends Component {
    static template = "awesome_owl.to_do_list";
    static components = {Item};

    setup() {
        const inputRef = useRef('tdinput');
        this.id = 1;
        this.items = useState([])
        onMounted(() => {
            inputRef.el.focus();
        });
    }

    add_to_list(ev) {
        if (ev.target.value !== "" && ev.keyCode === 13) {
            this.items.push({
                id: this.id,
                description: ev.target.value,
                isCompleted: false
            });
            this.id++;
            ev.target.value = "";
        }
    }
    findel(item){
        return item.id === this.id;
    }
    checkOne(itemId) {
        let rec=null;
        for(const item of this.items) {
            if (itemId === item.id) {
                rec=item;
                break;
            }
        }
        if (rec) {
            rec.isCompleted = !rec.isCompleted;
        }
    }
    rmItem(itemId) {
        for(let i = 0; i < this.items.length; i++) {
            if (itemId === this.items[i].id) {
                if (i===0)
                    this.items.shift(0);
                else
                    this.items.splice(i, i);
                break;
            }
        }

    }
}