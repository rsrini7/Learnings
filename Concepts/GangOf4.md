# Functional Programming Alternatives to the 23 Gang of Four (GoF) Design Patterns

Functional programming alternatives to the 23 Gang of Four (GoF) design patterns, emphasizing building connections and growing upon existing knowledge rather than dismissing older concepts.

## Creational Patterns
These patterns deal with object creation mechanisms.

### Abstract Factory: While not directly used in functional programming (FP), the concept is achieved through functions, polymorphic types, and type classes. Demonstrates this with Haskell's Beam and Persistent libraries, which abstract over database backends, allowing the selection of a specific backend (e.g., SQLite, PostgreSQL) at runtime.

### Factory Method: This pattern, common in Scala, aims to hide concrete implementations behind an abstraction or interface. The "tagless final" approach in Scala is presented as a functional alternative, using abstract interfaces for operations (like payment processing) and then providing specific implementations based on configuration (e.g., PayPal or Stripe).

### Singleton: In FP, singletons are often unnecessary due to immutability. Instances are typically created once and then passed as arguments to functions where they are needed. Haskell's withConnect function for database connections and Scala's singleton objects are discussed as parallels.

### Builder: This pattern is quite common in Scala and Haskell for constructing complex objects step-by-step. Examples include building HTTP requests using Scala's sttp library and deriving JSON codecs in Haskell. The concept of "smart constructors" in FP is introduced as a way to ensure only valid data is created.

### Prototype: This pattern involves creating new objects by copying a prototypical instance. This aligns well with functional programming's emphasis on copying data, as seen with default options in JSON libraries or using copy methods on case classes in Scala.

## Structural Patterns
These patterns deal with object composition and structure.

### Adapter: The Adapter pattern is used to convert one interface to another. In FP, this can involve adapting data types (e.g., InvoiceV1 to InvoiceV2) or integrating different API frameworks in Haskell using monad transformers like lift.io to bridge IO operations with more abstract monads like resource T.

### Bridge: This pattern aims to decouple an abstraction from its implementation, often by using composition instead of inheritance. Notes that in Haskell, this is sometimes achieved through internal modules that expose lower-level, less stable APIs, keeping the high-level interface separate from concrete details.

### Composite: This pattern composes objects into tree structures to represent part-whole hierarchies. In FP, trees and recursion are fundamental concepts. Type classes are used to model the composite pattern, providing a uniform interface for both individual components and compositions, as shown with a Printable type class example for JSON structures.

### Decorator: Decorators attach additional responsibilities to an object dynamically. In FP, this is often used to separate business logic from "bells and whistles" like metrics or caching, by wrapping existing functionalities with new ones.

### Facade: The presenter suggests that Facade is less of a distinct design pattern in FP and more about good design practices, where a simple interface provides a higher-level view of a complex subsystem.

### Flyweight: With immutability in FP, the Flyweight pattern (sharing fine-grained objects efficiently) can often be achieved implicitly. Because data is immutable, instances of expensive values are created only once and can be shared efficiently.

### Proxy: Structurally similar to Decorator, the Proxy pattern focuses on restricting access, providing lazy initialization, or adding security, rather than enhancing functionality.

## Behavioral Patterns
These patterns deal with communication and interaction between objects.

### Chain of Responsibility: This pattern allows passing a request along a chain of handlers. In FP, this is often implemented using Option types or types with Alternative instances to chain fallback mechanisms (e.g., trying different payment methods or parsing strategies) until a successful result is obtained.

### Command: The Command pattern encapsulates a request as an object, allowing parameterization of clients with different requests. In FP, commands are often represented by data types that describe computations, such as IO, Task, or Effect. Illustrates this by creating a function to repeat an arbitrary effectful computation n times and handling payment operations as a service pattern.

### Interpreter: This pattern defines a representation for a language's grammar along with an interpreter to use that representation. It is highly beloved in FP, often implemented through Embedded Domain Specific Languages (EDSLs). Demonstrates defining expressions and operations (like Add and Literal) with different evaluators (interpreters) for computation and pretty-printing.

### Iterator: This pattern provides a way to access elements of an aggregate object sequentially without exposing its underlying representation. In FP, this is largely handled by Foldable and Traversable type classes for applying functions over collections, and optics (like lenses) for navigating and modifying deeply nested data structures.

### Mediator: This pattern is used to reduce coupling between communicating objects. Briefly mentions that this pattern is often implemented implicitly in functional programming due to the explicit data flow and function composition, which naturally reduces direct dependencies.

### Memento: The Memento pattern is used to restore an object to its previous state (undo/redo functionality). In FP, this is achieved through immutable data structures and managing a history of states, often using abstractions like zippers for efficient navigation and modification of sequences while maintaining history.

### Observer: This pattern defines a one-to-many dependency, notifying dependents when an object's state changes. In FP, this is commonly replaced by Event Streams or Functional Reactive Programming (FRP). Shows using FS2 (a functional stream library) with primitives like Topic and Signal to implement publish-subscribe patterns.

### State: The State pattern allows an object to alter its behavior when its internal state changes. In FP, state is managed explicitly using constructs like State monads, often found in libraries like mtl or effectful. This involves passing state as an argument and returning new state, ensuring pure computations. Also touches on frontend frameworks like Elm that manage application state with models, views, and update functions.

### Strategy: This pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. In functional programming, this is inherently achieved by passing functions as arguments, as functions are first-class citizens. Different "strategies" are simply different functions that can be passed to a higher-order function.

### Template Method: This pattern defines the skeleton of an algorithm in a method, deferring some steps to subclasses. In functional programming, this is often accomplished using higher-order functions that take functions as arguments for the varying steps, or by using type classes to define generic interfaces that can be implemented differently.

### Visitor: The Visitor pattern allows adding new operations to existing object structures without modifying them. In functional programming, this is often achieved through pattern matching, where different cases of a data type are handled explicitly to apply specific behaviors based on the data' type of data.
---

Below is a **clean, systematic mapping of every classic GoF pattern to its functional-programming (FP) alternative**, distilled from the material you shared and aligned with real FP practice (Haskell / Scala / FP-in-JVM thinking).

The key idea: **FP does not “remove” patterns — it absorbs them into language features, types, and composition**.

---

Think of this as a **knowledge-transfer map**, not a replacement.

---

# Functional Programming Alternatives to the 23 GoF Patterns

*(Updated, complete, and aligned with modern FP practice)*

---

## I. Creational Patterns (5)

> **OO focus:** controlling *how objects are created*
> **FP focus:** controlling *how values and capabilities are constructed*

---

### 1. Abstract Factory

**OO intent:** Create families of related objects without specifying concrete classes

**FP alternative:**

* Parametric polymorphism
* Type classes / interfaces
* Capability algebras

**FP mapping:**

```text
Factory → Type class instance selection
```

**Modern FP examples:**

* DB backends via type classes (Beam, Persistent)
* HTTP clients via algebra + interpreter

**What’s new:**
👉 This is foundational for **hexagonal architecture** and **dependency inversion in FP**

---

### 2. Factory Method

**OO intent:** Delegate object creation to subclasses

**FP alternative:**

* Tagless Final
* Higher-order functions
* Module-level dependency injection

**FP mapping:**

```text
Factory Method → Algebra + interpreter chosen at runtime
```

**Modern usage:**

* Payment gateways
* Logging backends
* Cloud provider abstractions

---

### 3. Singleton

**OO intent:** Ensure a class has one instance

**FP alternative:**

* Immutability
* Explicit dependency passing
* Effect scoping (`Resource`, `withX`)

**FP mapping:**

```text
Singleton → Value created once & passed explicitly
```

**Update:**
Scala `object` is *syntactic*, but real FP avoids hidden globals.

---

### 4. Builder

**OO intent:** Step-by-step construction of complex objects

**FP alternative:**

* Smart constructors
* Immutable builders
* DSLs

**FP mapping:**

```text
Builder → Validated construction via pure functions
```

**Modern FP additions:**

* Refined types
* Validation via `Either` / `Validated`

---

### 5. Prototype

**OO intent:** Clone existing objects

**FP alternative:**

* Structural sharing
* Copy-on-write data
* Case class `.copy`

**FP mapping:**

```text
Prototype → Cheap immutable copying
```

---

## II. Structural Patterns (7)

> **OO focus:** object composition
> **FP focus:** function & data composition

---

### 6. Adapter

**OO intent:** Convert one interface into another

**FP alternative:**

* Pure transformation functions
* Natural transformations (`F ~> G`)

**FP mapping:**

```text
Adapter → A → B
```

**New addition:**
Adapters are often **lossless data migrations** in FP systems.

---

### 7. Bridge

**OO intent:** Separate abstraction from implementation

**FP alternative:**

* Module boundaries
* Algebra vs interpreter
* Internal vs public modules

**FP mapping:**

```text
Bridge → Stable algebra + swappable interpreter
```

---

### 8. Composite

**OO intent:** Treat individual objects and compositions uniformly

**FP alternative:**

* Recursive ADTs
* Type classes
* Catamorphisms (folds)

**FP mapping:**

```text
Composite → Recursive data + fold
```

---

### 9. Decorator

**OO intent:** Add behavior dynamically

**FP alternative:**

* Function wrapping
* Middleware
* Effect transformation

**FP mapping:**

```text
Decorator → f ∘ g ∘ h
```

**Modern FP usage:**

* Logging
* Metrics
* Retries
* Tracing

---

### 10. Facade

**OO intent:** Simplify a complex subsystem

**FP alternative:**

* Well-designed module API
* Smart constructors
* Re-exported interfaces

**Update:**
Facade is now considered **API design**, not a special pattern.

---

### 11. Flyweight

**OO intent:** Share objects to save memory

**FP alternative:**

* Immutability
* Referential transparency
* Structural sharing

**FP mapping:**

```text
Flyweight → Default FP memory model
```

---

### 12. Proxy

**OO intent:** Control access to an object

**FP alternative:**

* Laziness
* Effect suspension
* Capability restriction

**FP mapping:**

```text
Proxy → Delayed or restricted effect execution
```

---

## III. Behavioral Patterns (11)

> **OO focus:** object interaction
> **FP focus:** data flow & effects

---

### 13. Chain of Responsibility

**OO intent:** Pass request along handlers

**FP alternative:**

* `Option`, `Either`
* `Alternative`
* Folds

**FP mapping:**

```text
Chain → firstSuccess(f1, f2, f3)
```

---

### 14. Command

**OO intent:** Encapsulate a request

**FP alternative:**

* Effects as data (`IO`, `Task`)
* Free monads / Tagless Final

**FP mapping:**

```text
Command → Program value
```

---

### 15. Interpreter

**OO intent:** Define grammar + interpreter

**FP alternative:**

* EDSLs
* Multiple interpreters
* Free / Tagless Final

**FP mapping:**

```text
Interpreter → Algebra + multiple semantics
```

---

### 16. Iterator

**OO intent:** Sequential access

**FP alternative:**

* `Foldable`
* `Traversable`
* Streams

**FP mapping:**

```text
Iterator → fold / map / traverse
```

---

### 17. Mediator

**OO intent:** Reduce coupling between objects

**FP alternative:**

* Explicit data flow
* Pure orchestration functions
* Event streams

**Update:**
Often **disappears entirely** in FP due to explicit wiring.

---

### 18. Memento

**OO intent:** Capture and restore state

**FP alternative:**

* Immutable history
* Persistent data structures
* Zippers

**FP mapping:**

```text
Memento → previousValue :: history
```

---

### 19. Observer

**OO intent:** Publish-subscribe

**FP alternative:**

* Streams
* FRP
* Signals

**FP mapping:**

```text
Observer → Event stream
```

---

### 20. State

**OO intent:** Change behavior based on state

**FP alternative:**

* State monad
* Explicit state passing
* Reducer pattern (Elm/Redux)

**FP mapping:**

```text
State → (S) → (A, S)
```

---

### 21. Strategy

**OO intent:** Interchange algorithms

**FP alternative:**

* Higher-order functions

**FP mapping:**

```text
Strategy → Function parameter
```

---

### 22. Template Method

**OO intent:** Algorithm skeleton with overridable steps

**FP alternative:**

* Higher-order functions
* Type classes

**FP mapping:**

```text
Template → function with hooks
```

---

### 23. Visitor

**OO intent:** Add operations without modifying structures

**FP alternative:**

* Pattern matching
* Folds
* Type-class-based extensibility

**FP mapping:**

```text
Visitor → match / fold
```

---

## Important “Not GoF but Commonly Asked”

| Pattern              | FP Status              |
| -------------------- | ---------------------- |
| Null Object          | `Option` / `Maybe`     |
| Dependency Injection | Function parameters    |
| Service Locator      | ❌ Anti-pattern in FP   |
| Active Object        | Async effects          |
| MVC                  | Elm Architecture / MVU |

---

## Final Mental Model

| GoF (OO)       | FP                 |
| -------------- | ------------------ |
| Objects        | Values             |
| Inheritance    | Composition        |
| Runtime wiring | Compile-time types |
| Patterns       | Language features  |

> **FP doesn’t reject GoF — it *internalizes* it into the type system.**

---

# Functional Alternatives to GoF Design Patterns

---

## 1. Creational Patterns → *Construction via Types & Functions*

| GoF Pattern          | What it Solves (OO view)         | Functional Alternative                                | Key FP Idea                             |
| -------------------- | -------------------------------- | ----------------------------------------------------- | --------------------------------------- |
| **Abstract Factory** | Families of related objects      | **Functions + parametric polymorphism + typeclasses** | Behavior chosen by types, not factories |
| **Factory Method**   | Hide concrete implementations    | **Tagless Final / Higher-order functions**            | Implementation passed as capability     |
| **Singleton**        | Single global instance           | **Immutability + explicit dependency passing**        | No mutable global state needed          |
| **Builder**          | Step-by-step object construction | **Smart constructors + immutable data + DSLs**        | Construction as pure transformation     |
| **Prototype**        | Copy existing object             | **Structural sharing + data copying**                 | Copy is cheap and safe                  |

### FP Insight

> Creation logic becomes **type-driven**, not object-driven.

---

## 2. Structural Patterns → *Composition over Structure*

| GoF Pattern   | OO Goal                               | Functional Alternative                          | Key FP Mechanism                   |
| ------------- | ------------------------------------- | ----------------------------------------------- | ---------------------------------- |
| **Adapter**   | Make interfaces compatible            | **Pure conversion functions**                   | `A → B` transformations            |
| **Bridge**    | Separate abstraction & implementation | **Module boundaries + parametric polymorphism** | Stable API over unstable internals |
| **Composite** | Tree-like structures                  | **Recursive ADTs + typeclasses**                | Data defines structure             |
| **Decorator** | Add responsibilities dynamically      | **Function wrapping / middleware**              | Behavior composition               |
| **Facade**    | Simplified interface                  | **Well-designed module API**                    | Just good FP design                |
| **Flyweight** | Share heavy objects                   | **Immutability + referential transparency**     | Sharing is automatic               |
| **Proxy**     | Access control / laziness             | **Lazy values / effect suspension**             | Execution control via effects      |

### FP Insight

> **Functions compose more naturally than objects wrap.**

---

## 3. Behavioral Patterns → *Data + Effects*

| GoF Pattern                 | OO Purpose               | Functional Equivalent                        | FP Primitive                      |
| --------------------------- | ------------------------ | -------------------------------------------- | --------------------------------- |
| **Chain of Responsibility** | Sequential handlers      | **`Option`, `Either`, `Alternative`, folds** | Short-circuiting composition      |
| **Command**                 | Encapsulate actions      | **Data describing effects (`IO`, `Task`)**   | Programs as values                |
| **Strategy**                | Swap algorithms          | **Higher-order functions**                   | Functions *are* strategies        |
| **Observer**                | Event subscription       | **Streams / Signals / Effects**              | Time-varying values               |
| **State**                   | Mutable behavior         | **State monad / explicit state passing**     | Controlled mutation               |
| **Iterator**                | Traverse collections     | **Lazy sequences / folds**                   | Pull-based computation            |
| **Template Method**         | Fixed algorithm skeleton | **Higher-order functions**                   | Behavior injected, not overridden |
| **Visitor**                 | Operations over data     | **Pattern matching + ADTs**                  | Data-driven dispatch              |
| **Memento**                 | Snapshot state           | **Persistent data structures**               | History for free                  |

### FP Insight

> **Behavior becomes data**, not objects with hidden mutation.

---

## 4. One-Line Mental Model Shift

| OO Thinking          | FP Thinking                 |
| -------------------- | --------------------------- |
| Objects own behavior | Functions transform data    |
| Inheritance          | Composition                 |
| Runtime polymorphism | Compile-time type selection |
| Design patterns      | Language features           |

---

## 5. Why FP “Needs Fewer Patterns”

The GoF book exists because **OO languages lacked**:

* Algebraic data types
* Pattern matching
* Higher-order functions
* Immutability by default
* First-class effects

FP languages **bake solutions directly into the type system**.

> In FP, **patterns are not abstractions you build — they are constraints you encode in types**.

---

## 6. Practical Takeaway for Developers

If you are designing in FP:

* ❌ Don’t ask: *“Which GoF pattern should I use?”*
* ✅ Ask: *“What does my type system need to guarantee?”*

---



