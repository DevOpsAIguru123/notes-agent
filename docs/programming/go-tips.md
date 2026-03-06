# Go Programming Tips

## Getting Started

- Use `go mod init <module-name>` to start a new project with module support.
- Run `go fmt ./...` before committing — consistent formatting is a core Go convention.
- Use `go vet ./...` to catch subtle bugs the compiler won't flag.

## Error Handling

- Always check returned errors. Ignoring them with `_` leads to silent failures.
- Wrap errors with context using `fmt.Errorf("doing X: %w", err)` so you can trace the cause up the call stack.
- Use `errors.Is()` and `errors.As()` instead of direct comparison for unwrapping wrapped errors.

## Structs and Interfaces

- Keep interfaces small — one or two methods is ideal. The `io.Reader` and `io.Writer` interfaces are great examples.
- Accept interfaces, return structs. This makes your code flexible for callers while keeping return types concrete.
- Use pointer receivers when methods need to modify the receiver or when the struct is large.

## Concurrency

- Don't communicate by sharing memory; share memory by communicating (use channels).
- Always know who is responsible for closing a channel — typically the sender.
- Use `sync.WaitGroup` to wait for multiple goroutines to finish.
- Avoid goroutine leaks by ensuring goroutines have a way to exit (e.g., a `done` channel or `context.Context`).
- Prefer `context.Context` for cancellation and timeouts over manual channel signaling.

## Slices and Maps

- Pre-allocate slices with `make([]T, 0, capacity)` when you know the expected size to reduce allocations.
- Maps are not safe for concurrent use — protect them with `sync.Mutex` or use `sync.Map`.
- Use `copy()` to clone a slice; assigning one slice to another shares the underlying array.

## Testing

- Name test files `*_test.go` — they are automatically excluded from production builds.
- Use table-driven tests to cover multiple cases cleanly.
- Run `go test -race ./...` to detect race conditions in concurrent code.
- Use `t.Helper()` in test helper functions so failure messages point to the caller.

## Performance

- Use `go test -bench=. -benchmem` to benchmark and track allocations.
- Avoid premature optimization — profile first with `pprof` to find real bottlenecks.
- Use `strings.Builder` instead of `+` for concatenating many strings.
- Prefer `sync.Pool` for frequently allocated and discarded objects to reduce GC pressure.

## Common Patterns

- Use `defer` for cleanup (closing files, unlocking mutexes) — it runs when the surrounding function returns.
- Use blank identifier `_` to verify interface compliance at compile time: `var _ MyInterface = (*MyStruct)(nil)`.
- Use `init()` sparingly — it runs automatically and can make code harder to reason about.
- Embed structs for composition over inheritance.
