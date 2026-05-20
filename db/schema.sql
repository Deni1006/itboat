CREATE TABLE IF NOT EXISTS yacht_listings (
    id UInt64,
    title String,
    price Float64,
    currency String,
    url String,
    images String,
    source String,
    collected_at DateTime
) ENGINE = MergeTree()
ORDER BY collected_at;
