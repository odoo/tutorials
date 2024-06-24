// /** @odoo-module **/

export const migrations = [
    {
        fromVersion: 0,
        toVersion: 1,
        apply(model) {
            console.log("Adding peach value");
            model.peachTreeCount = 0;
            model.peachFruitCount = 0;
        },
    },
];
