/** @odoo-module **/

import { useRef, onMounted } from "@odoo/owl";

function useAutoFocus(element_ref){
    let inputRef = useRef(element_ref);
    onMounted(() => {
        inputRef.el.focus();
    });
}

export { useAutoFocus };
