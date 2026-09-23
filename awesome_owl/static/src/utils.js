import {onMounted} from "@odoo/owl"


export function useAutoFocus(ref) {
    onMounted(() => {
        console.log(ref)
        ref.el.focus()
    })
}