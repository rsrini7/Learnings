# Java Remote Debugging

We use a Socket Attaching Connector, which is enabled by default when the `dt_socket` transport is configured and the VM is running in the server debugging mode.

## Java Environment Variable

Append `$JAVA_OPTS` or `%JAVA_OPTS%` if required:

```bash
JAVA_OPTS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"
```

## Java Versions

### For Java 9 or above

Since Java 9.0, JDWP supports only local connections by default. Add `*:<port>` to listen on all interfaces:

```bash
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 <AppJar>
```

### For Java 1.5 to 1.8

```bash
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 <AppJar>
```

### For Java 1.4

Before Java 5.0, use `-Xdebug` and `-Xrunjdwp` arguments. These options will still work in later versions, but it will run in interpreted mode instead of JIT, which will be slower.

```bash
java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005 <AppJar>
```

### For Java 1.3

```bash
java -Xnoagent -Djava.compiler=NONE -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005 <AppJar>
```

## Build Tools Configuration

### For Spring Maven

```bash
mvn spring-boot:run -Drun.jvmArguments="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005"
```

### For Spring Gradle

```bash
gradle bootrun --debug-jvm
```

## Docker

```bash
docker run -it -e JAVA_OPTS='-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005' -p 5005:5005 <image>
```

## JDWP Argument Options

Options on `-Xrunjdwp` or `agentlib:jdwp` arguments are:

*   `transport=dt_socket`: Specifies the way used to connect to the JVM (socket is a good choice, it can be used to debug a distant computer).
*   `address=5005`: The TCP/IP port exposed, to connect from the debugger.
*   `suspend=y`: If 'y', tells the JVM to wait until the debugger is attached to begin execution; otherwise (if 'n'), starts execution right away.

It is not required to add the `address` parameter. If not provided, the agent selects a random port number. This might be useful if you start multiple nodes within the same Java command line.
