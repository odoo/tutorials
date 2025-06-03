/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl";

export function useAutoFocus(refname) {
    console.log(`useAutoFocus called with refname: ${refname}`);
    const inputRef = useRef(refname)

    onMounted(() => {
       if (inputRef.el) {
            inputRef.el.focus();
            console.log(`Input with ref '${refname}' has been focused.`);
        }
        else {
            console.warn(`Input with ref '${refname}' not found.`);
        }
    });
}