export const migrations = [
    {
        fromVersion : 0,
        toVersion: 1,
        apply(model){
            console.log(`Upgrades to ${this.toVersion}`)
            return model;
        }
    },
    {
        fromVersion : 1,
        toVersion: 2,
        apply(model)
        {
            model.trees = Object.assign(model.trees,
            {
                peach: {
                    quantity:0,
                    fruit:0,
                    price:10000
                }
            })
            return model;
        }
    }

]
export const CURENTVERSION = 2;

export function migrate(model)
{

    if (model.version == CURENTVERSION)
    {
        return model;
    }

    if (!model.version)
    {
        model = Object.assign(model, {version:0});
    }

    for (const migration in migrations)
        {
            if(migrations[migration].fromVersion == model.version)
            {
                model = migrations[migration].apply(model);
                console.log(`Upgraded from version ${model.version} to ${migrations[migration].toVersion}`)
                model.version = migrations[migration].toVersion;
                if(model.version == CURENTVERSION)
                {
                    return model;
                }
            }
        }
    console.log(`Couldn't fully upgrade model ${model.version} < ${CURENTVERSION}`);
    return model;
}
