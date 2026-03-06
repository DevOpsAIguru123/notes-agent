# JavaScript Tips

## Modern Syntax (ES6+)

### Destructuring

```javascript
// Object destructuring
const { name, age, city = "Unknown" } = user;

// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];

// Function parameters
function greet({ name, role = "user" }) {
  return `Hello ${name} (${role})`;
}
```

### Template Literals

```javascript
const message = `Hello ${name},
You have ${count} new messages.
Total: ${price * quantity}`;
```

### Optional Chaining & Nullish Coalescing

```javascript
// Optional chaining - safe deep access
const city = user?.address?.city;
const first = arr?.[0];
const result = obj?.method?.();

// Nullish coalescing - default only for null/undefined
const port = config.port ?? 3000;
const name = user.name ?? "Anonymous";
```

## Async Patterns

### Promises vs Async/Await

```javascript
// Promise chaining
fetch("/api/users")
  .then(res => res.json())
  .then(users => console.log(users))
  .catch(err => console.error(err));

// Async/await (preferred)
async function getUsers() {
  try {
    const res = await fetch("/api/users");
    const users = await res.json();
    return users;
  } catch (err) {
    console.error("Failed to fetch users:", err);
  }
}
```

### Parallel Execution

```javascript
// Run independent async tasks in parallel
const [users, posts, comments] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
  fetchComments(),
]);

// Promise.allSettled - don't fail if one rejects
const results = await Promise.allSettled([task1(), task2(), task3()]);
results.forEach(r => {
  if (r.status === "fulfilled") console.log(r.value);
  else console.error(r.reason);
});
```

## Array Methods Cheat Sheet

```javascript
const numbers = [1, 2, 3, 4, 5];

numbers.map(n => n * 2);           // [2, 4, 6, 8, 10]
numbers.filter(n => n > 3);        // [4, 5]
numbers.reduce((sum, n) => sum + n, 0); // 15
numbers.find(n => n > 3);          // 4
numbers.some(n => n > 4);          // true
numbers.every(n => n > 0);         // true
numbers.flatMap(n => [n, n * 10]); // [1, 10, 2, 20, ...]
```

## Common Gotchas

| Gotcha | Problem | Fix |
|--------|---------|-----|
| `==` vs `===` | `0 == ""` is true | Always use `===` |
| `this` in callbacks | Loses context | Use arrow functions |
| Floating point | `0.1 + 0.2 !== 0.3` | Round or use integers |
| Array copy | `b = a` shares reference | `b = [...a]` or `structuredClone(a)` |
| `typeof null` | Returns `"object"` | Check `val === null` explicitly |
