# Java Baseline Requirements - Spring Boot 4

## Requirement
**Spring Boot 4.0 requires Java 21 minimum** (LTS release)

## Why Java 21?
- Spring Framework 7 requires Java 21+
- Jakarta EE 11 baseline requires Java 21+
- Virtual threads & ZGC (JDK 21 features) optimal for Spring Boot 4
- Java 20 and earlier NOT supported

## Installation

### macOS (Homebrew)
```bash
brew install openjdk@21
echo 'export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
java -version  # Verify: openjdk 21.x.x
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install openjdk-21-jdk
java -version  # Verify: openjdk 21.x.x
```

### Windows
```powershell
# Using Chocolatey
choco install openjdk21

# Or download from https://adoptium.net/
# Install and set JAVA_HOME environment variable
java -version  # Verify: openjdk 21.x.x
```

### SDKMAN (All platforms)
```bash
curl -s "https://get.sdkman.io" | bash
sdk list java | grep 21
sdk install java 21.0.1-tem
java -version
```

## Update Maven/Gradle

### Maven (pom.xml)
```xml
<properties>
    <java.version>21</java.version>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
</properties>
```

### Gradle (build.gradle)
```gradle
java {
    sourceCompatibility = '21'
    targetCompatibility = '21'
}
```

## Verification
```bash
java -version
# Expected: openjdk 21.0.x (or similar)

./mvnw --version
# Expected: Maven 3.9.0+

./gradlew --version
# Expected: Gradle 8.4+
```

## If You See Errors
- **"javac: invalid release version 21"** → Java 21 not installed
- **"Error: Could not find or load main class"** → Check JAVA_HOME env var
- **"Spring Boot 4 not found"** → Maven/Gradle cache issue, run `clean install`
