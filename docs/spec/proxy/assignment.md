# `proxy::operator=`

```cpp
// (1)
proxy& operator=(std::nullptr_t)
    noexcept(F::destructibility >= constraint_level::nothrow)
    requires(F::destructibility >= constraint_level::nontrivial);

// (2)
proxy& operator=(const proxy&) noexcept requires(F::copyability ==
    constraint_level::trivial) = default;
proxy& operator=(const proxy& rhs)
    noexcept(F::copyability >= constraint_level::nothrow &&
        F::destructibility >= constraint_level::nothrow)
    requires((F::copyability == constraint_level::nontrivial ||
        F::copyability == constraint_level::nothrow) &&
        F::destructibility >= constraint_level::nontrivial);

// (3)
proxy& operator=(proxy&& rhs)
    noexcept(F::relocatability >= constraint_level::nothrow &&
        F::destructibility >= constraint_level::nothrow)
    requires(F::relocatability >= constraint_level::nontrivial &&
        F::destructibility >= constraint_level::nontrivial &&
        F::copyability != constraint_level::trivial);

// (4)
template <class P>
proxy& operator=(P&& ptr)
    noexcept(std::is_nothrow_constructible_v<std::decay_t<P>, P> &&
        F::destructibility >= constraint_level::nothrow)
    requires(std::is_constructible_v<std::decay_t<P>, P> &&
        F::destructibility >= constraint_level::nontrivial);
```

Assigns a new value to `proxy` or destroys the contained value.

- `(1)` Destroys the current contained value if it exists. After the call, `*this` does not contain a value.
- `(2)` Copy assignment operator copies the contained value of `rhs` to `*this`. If `rhs` does not contain a value, it destroys the contained value of `*this` (if any) as if by `auto(rhs).swap(*this)`. The copy assignment is trivial when `F::copyability == constraint_level::trivial` is `true`.
- `(3)` Move assignment operator moves the contained value of `rhs` to `*this`. If `rhs` does not contain a value, it destroys the contained value of `*this` (if any). If the move construction throws when `F::relocatability == constraint_level::nontrivial`, `*this` does not contain a value. After move assignment, `rhs` is in a valid state with an unspecified value. The move assignment operator does not participate in overload resolution when `F::copyability == constraint_level::trivial`, falling back to the trivial copy assignment operator.
- `(4)` Let `VP` be `std::decay_t<P>`. Sets the contained value to an object of type `VP`, direct-non-list-initialized with `std::forward<P>(ptr)`. This overload participates in overload resolution only if `std::decay_t<P>` is not a specialization of `proxy`. *Since 3.3.0*: If [`proxiable<VP, F>`](../proxiable.md) is `false`, the program is ill-formed and diagnostic messages are generated.

## Return Value

`*this`.
