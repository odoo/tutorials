import { onMounted, useRef } from "@odoo/owl"

export function useAutofocus() {

    const inputRef = useRef("input")
    onMounted(() => {
        if (inputRef.el) {
            inputRef.el.focus()
        }
    })

    return inputRef;

}
