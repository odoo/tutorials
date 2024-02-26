/** @odoo-module **/

import { useRef,onMounted} from "@odoo/owl";

export function focus_element(refName) {
    const ref=useRef(refName);
    onMounted(()=>{ref.el.focus();});
}
