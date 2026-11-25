package com.foodbridge;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

final class Models {
    static final List<String> ROLES = List.of("Citizen", "Food Donor", "NGO", "Volunteer");
    static final List<String> CATEGORIES = List.of("Cooked meals", "Fresh produce", "Bakery", "Pantry");

    @Entity(name = "Account") @Table(name = "accounts")
    static class Account {
        @Id @Column(length = 36) String id = UUID.randomUUID().toString();
        @Column(nullable = false, length = 80) String name;
        @Column(nullable = false, unique = true, length = 150) String email;
        @Column(nullable = false, length = 100) String passwordHash;
        @Column(nullable = false, length = 30) String role;
        @Column(nullable = false, length = 100) String organization = "";
        @Column(nullable = false, length = 80) String area = "Indiranagar";
        public String getId() { return id; }
        public String getName() { return name; }
    }

    @Entity(name = "FoodDonation") @Table(name = "donations")
    static class FoodDonation {
        @Id @Column(length = 36) String id = UUID.randomUUID().toString();
        @Column(nullable = false, length = 100) String name;
        @Column(nullable = false, length = 30) String category;
        @Column(nullable = false, length = 2000) String description;
        @Column(nullable = false) int quantity;
        @Column(nullable = false, length = 30) String unit;
        @Column(nullable = false, length = 250) String location;
        @Column(nullable = false, length = 80) String area;
        @Column(nullable = false) double distance;
        @Column(nullable = false) Instant preparedAt;
        @Column(nullable = false) Instant deadline;
        @org.hibernate.annotations.JdbcTypeCode(org.hibernate.type.SqlTypes.LONGVARCHAR)
        @Column(nullable = false, columnDefinition = "LONGTEXT") String image;
        @Column(nullable = false, length = 100) String donor;
        @Column(nullable = false, length = 250) String dietary;
        @Column(nullable = false, length = 250) String allergens;
        @ManyToOne(optional = false, fetch = FetchType.LAZY) @JoinColumn(name = "owner_id") Account owner;
        @Column(nullable = false) boolean claimed;
        @Column(nullable = false) Instant createdAt = Instant.now();
        public String getId() { return id; }
        public Account getOwner() { return owner; }
        public Instant getDeadline() { return deadline; }
    }

    @Entity(name = "Pickup") @Table(name = "pickups")
    static class Pickup {
        @Id @Column(length = 36) String id = UUID.randomUUID().toString();
        @OneToOne(optional = false, fetch = FetchType.LAZY) @JoinColumn(name = "donation_id", unique = true) FoodDonation donation;
        @ManyToOne(optional = false, fetch = FetchType.LAZY) @JoinColumn(name = "recipient_id") Account recipient;
        @ManyToOne(fetch = FetchType.LAZY) @JoinColumn(name = "volunteer_id") Account volunteer;
        @Column(nullable = false) int stage = 1;
        @Column(nullable = false) Instant createdAt = Instant.now();
        @ElementCollection @CollectionTable(name = "pickup_timestamps", joinColumns = @JoinColumn(name = "pickup_id"))
        @OrderColumn(name = "stage_index") @Column(name = "occurred_at", nullable = false)
        List<Instant> timestamps = new ArrayList<>();
    }
}
