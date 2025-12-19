
Base
### 1\. Initial Compilation & Size Comparison

**Timestamp:** [[00:44](http://www.youtube.com/watch?v=IXBaXyLdrTA&t=44)]
The narrator compiles a basic "Hello World" program in both Rust and C.

  * **Commands:**
    ```bash
    rustc main.rs -o hello_r
    gcc main.c -o hello_c
    ls -lh  # (Implied command to check file size)
    ```
  * **Output:**
      * `hello_r` (Rust): **\~3.9 MB** (described as "almost 4 megabytes").
      * `hello_c` (C): **\~15 KB**.

### 2\. Crash Handling Test

**Timestamp:** [[01:01](http://www.youtube.com/watch?v=IXBaXyLdrTA&t=61)]
Both programs are modified to access an array out of bounds to trigger a crash.

  * **C Crash:**
      * **Command:** `./hello_c`
      * **Output:** `Segmentation fault` (or similar OS-level crash message). The narrator notes it "doesn't really tell you where we crashed."
  * **Rust Crash:**
      * **Command:** `./hello_r`
      * **Output:**
        ```text
        thread 'main' panicked at 'index out of bounds: the len is 1 but the index is 10'
        note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
        ```
      * **Follow-up Command:** `RUST_BACKTRACE=full ./hello_r`
      * **Output:** Displays a detailed stack trace pointing to the exact line of failure.

### 3\. Reducing Binary Size (Stripping Debug Info)

**Timestamp:** [[03:26](http://www.youtube.com/watch?v=IXBaXyLdrTA&t=206)]
The narrator explains that Rust binaries include debug symbols by default, unlike C (in this context).

  * **Command:**
    ```bash
    rustc -C strip=debuginfo main.rs
    ```
  * **Output:**
      * The binary size drops to **\~400 KB** (down from \~4 MB).

### 4\. Inspecting Symbols & Linking

**Timestamp:** [[04:25](http://www.youtube.com/watch?v=IXBaXyLdrTA&t=265)]
The narrator uses `objdump` and `ldd` to inspect the binaries.

  * **Commands:**
    ```bash
    ldd hello_c
    ldd hello_r
    objdump -t hello_r  # (Implied flags for symbol table)
    ```
  * **Output:**
      * **C:** Dynamically links to `libc`. Has very few symbols.
      * **Rust:** Statically links the Rust standard library (`libstd`). Contains many symbols (e.g., mangled names like `_ZN4...`) because the library code is baked into the executable.

### 5\. Dynamic Linking in Rust

**Timestamp:** [[05:46](http://www.youtube.com/watch?v=IXBaXyLdrTA&t=346)]
To make a "fair" comparison, the narrator compiles Rust to link dynamically against `libstd`, just like C links against `libc`.

  * **Command:**
    ```bash
    rustc -C prefer-dynamic=yes main.rs
    ```
  * **Output:**
      * The binary size drops to **\~8 KB** (now smaller than the 15 KB C program).

### 6\. Running the Dynamically Linked Rust Binary

**Timestamp:** [[06:51](http://www.youtube.com/watch?v=IXBaXyLdrTA&t=411)]
Trying to run the tiny Rust binary fails because the system cannot find the shared Rust library.

  * **Command:** `./hello_r`
  * **Output:**
    ```text
    error while loading shared libraries: libstd-[hash].so: cannot open shared object file: No such file or directory
    ```

### 7\. Fixing the Path & Final Run

**Timestamp:** [[07:38](http://www.youtube.com/watch?v=IXBaXyLdrTA&t=458)]
To run the dynamically linked binary, the library path must be provided.

  * **Command:**
    ```bash
    # Path is found in the toolchain directory (e.g., ~/.rustup/toolchains/...)
    export LD_LIBRARY_PATH=/path/to/rust/lib
    ./hello_r
    ```
    *(Alternatively prepended: `LD_LIBRARY_PATH=... ./hello_r`)*
  * **Output:**
      * `Hello, world!` (The program runs successfully).

Source: https://www.youtube.com/watch?v=IXBaXyLdrTA
