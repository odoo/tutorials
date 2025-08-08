import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(ref){
    const inputRef = useRef(ref)

    onMounted(() => {
        if(inputRef.el){
            inputRef.el.focus();
        }
    });
}
