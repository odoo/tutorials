import { onMounted, useRef } from "@odoo/owl";


export function useAutofocus(refLabel) {
    let inputRef = useRef(refLabel);

    onMounted(() => {
        console.log(inputRef.el);
        inputRef.el.focus();
    });
    return inputRef;
}
