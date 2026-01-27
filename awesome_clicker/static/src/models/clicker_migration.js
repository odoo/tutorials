export const currentVersion = 1;

const migrations = [
    {
        fromVersion: 1,
        toVersion: 2,
        apply(clicker) {
            clicker.trees.push(0);
            clicker.fruits.push(0);
        }
    }
]

export function migrate(clicker) {
    let didMigrate = false;

    for(let migration of migrations) {
        if(migration.fromVersion === clicker.version) {
            migration.apply(clicker);
            clicker.version = migration.toVersion;

            didMigrate = true;
        }
    }

    return didMigrate;
}
