# NoSQL Concepts

## Types of NoSQL Databases

### Document Store (MongoDB)

Stores data as flexible JSON-like documents. Great for content management, user profiles, and catalogs.

```javascript
// MongoDB document
{
  _id: ObjectId("..."),
  name: "Alice",
  email: "alice@example.com",
  addresses: [
    { type: "home", city: "Seattle", zip: "98101" },
    { type: "work", city: "Bellevue", zip: "98004" }
  ],
  orders: [
    { product: "Laptop", price: 999, date: ISODate("2025-03-01") }
  ]
}
```

```javascript
// Common queries
db.users.find({ "addresses.city": "Seattle" });
db.users.find({ age: { $gte: 18, $lte: 65 } });
db.orders.aggregate([
  { $group: { _id: "$product", total: { $sum: "$price" } } },
  { $sort: { total: -1 } }
]);
```

### Key-Value Store (Redis)

Simple key-to-value mapping. Extremely fast for caching, sessions, and counters.

```bash
# Strings
SET user:1:name "Alice"
GET user:1:name

# Hash (like a mini document)
HSET user:1 name "Alice" email "alice@example.com"
HGETALL user:1

# Lists (queues)
LPUSH tasks "send_email"
RPOP tasks

# Sets
SADD online_users "alice" "bob"
SISMEMBER online_users "alice"  # true

# Expiry (TTL)
SET session:abc123 "user_data" EX 3600  # Expires in 1 hour
```

### Graph Database (Neo4j)

Models relationships as first-class citizens. Ideal for social networks, recommendation engines.

```cypher
// Create nodes and relationships
CREATE (alice:Person {name: "Alice"})
CREATE (bob:Person {name: "Bob"})
CREATE (alice)-[:FOLLOWS]->(bob)

// Find friends of friends
MATCH (me:Person {name: "Alice"})-[:FOLLOWS]->()-[:FOLLOWS]->(fof)
WHERE fof <> me
RETURN DISTINCT fof.name
```

## SQL vs NoSQL Decision Guide

| Factor | Choose SQL | Choose NoSQL |
|--------|-----------|-------------|
| Schema | Well-defined, stable | Evolving, flexible |
| Transactions | Critical (banking) | Eventual consistency OK |
| Queries | Complex joins needed | Simple lookups, aggregations |
| Scale | Vertical (bigger server) | Horizontal (more servers) |
| Data shape | Tabular, normalized | Nested, denormalized |

## Data Modeling in NoSQL

### Embedding vs Referencing

```javascript
// Embedded (denormalized) - fast reads, data duplication
{
  name: "Blog Post",
  author: { name: "Alice", avatar: "alice.png" },
  comments: [
    { user: "Bob", text: "Great post!" }
  ]
}

// Referenced (normalized) - no duplication, extra queries
{
  name: "Blog Post",
  author_id: ObjectId("..."),
  comment_ids: [ObjectId("..."), ObjectId("...")]
}
```

!!! tip "Rule of Thumb"
    Embed when data is read together and rarely changes independently. Reference when data is shared across documents or updated frequently.

## CAP Theorem

You can only guarantee two of three in a distributed system:

- **Consistency** - Every read gets the latest write
- **Availability** - Every request gets a response
- **Partition tolerance** - System works despite network failures

| Database | CAP Choice |
|----------|-----------|
| PostgreSQL | CA (single node) |
| MongoDB | CP (consistency + partition tolerance) |
| Cassandra | AP (availability + partition tolerance) |
| Redis | CP (with clustering) |
