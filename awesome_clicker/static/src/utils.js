/** @odoo-module **/

export function randomInt(max) {
    return Math.floor(Math.random() * max);
}

export function choose(array) {
    return array[randomInt(array.length)];
}

export function migrationUpdate(migrations, model, oldVersion, newVersion) {
    const requiredMigrations = migrations.filter(
        (migration) => migration.fromVersion === oldVersion && migration.toVersion === newVersion
    );
    console.log(requiredMigrations);
    return requiredMigrations.reduce((acc, val) => val.apply(acc), model);
}
