export function clickAddQuantity() {
    return [
        {
            isActive: ["desktop"],
            content: "click Add Quantity button",
            trigger: 'button:contains("Add Quantity")',
            run: "click",
        },
        {
            isActive: ["mobile"],
            content: "click Add Quantity button",
            trigger: 'button:contains("Add Quantity")',
            run: "click",
        },
    ];
}
export function fillInputArea(target, value) {
    return {
        content: `Fill input area with ${value}`,
        trigger: `input${target}`,
        run: `edit ${value}`,
    };
}
