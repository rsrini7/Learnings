# Spring Data Updates

## JPA Repository

All Spring Data JPA repositories work the same, but use jakarta.persistence.* packages.

```java
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import org.springframework.data.jpa.repository.JpaRepository;

@Entity
public class Order {
    @Id
    @GeneratedValue
    private Long id;
    private String customerName;
}

public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByCustomerName(String name);
}
```

## No Breaking Changes

Spring Data works the same in Spring Boot 4, just ensure:
- Use jakarta.persistence.* imports
- Update to Hibernate 6.4 (automatic with Boot 4)
