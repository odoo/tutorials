/** @odoo-module **/

import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(name) {
    var inputRef = useRef(name);
    onMounted(()=> {
        inputRef.el.focus();
    });
}
