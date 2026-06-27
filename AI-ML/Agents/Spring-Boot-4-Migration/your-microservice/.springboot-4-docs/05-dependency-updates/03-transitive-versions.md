# Transitive Dependency Versions

## Key Transitive Dependencies

| Dependency | Spring Boot 3 | Spring Boot 4 |
|------------|--------------|--------------|
| Spring Framework | 6.0.x | 7.0.x |
| Hibernate | 6.2.x | 6.4.x |
| Jackson | 2.15.x | 2.16.x |
| Tomcat | 10.1.x | 11.0.x |
| Netty | 4.1.x | 4.1.x |
| Reactor | 2022.0.x | 2023.0.x |

## Conflict Resolution

If you encounter version conflicts, use dependency management:

### Maven
```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.16.0</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### Gradle
```gradle
ext {
    jacksonVersion = '2.16.0'
}

dependencies {
    implementation "com.fasterxml.jackson.core:jackson-databind:${jacksonVersion}"
}
```
