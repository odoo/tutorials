/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl";

function useAutoFocus(elementRef){
    let inputRef = useRef(elementRef);
    onMounted(() => {
        inputRef.el.focus();
    });
}

export { useAutoFocus };
