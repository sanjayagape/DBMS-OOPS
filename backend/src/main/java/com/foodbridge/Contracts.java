package com.foodbridge;

import com.foodbridge.Models.*;
import jakarta.validation.constraints.*;
import java.time.Instant;
import java.util.List;

final class Contracts {
    record Register(@NotBlank @Size(min=2,max=80) String name, @NotBlank @Email @Size(max=150) String email,
                    @NotBlank @Size(min=8,max=72) String password, @NotBlank String role) {}
    record Login(@NotBlank @Email @Size(max=150) String email, @NotBlank @Size(max=72) String password) {}
    record Profile(@NotBlank @Size(min=2,max=80) String name, @NotNull @Size(max=100) String organization,
                   @NotBlank @Size(max=80) String area) {}
    record NewDonation(@NotBlank @Size(max=100) String name, @NotBlank String category,
                       @NotBlank @Size(max=2000) String description, @Min(1) @Max(100000) int quantity,
                       @NotBlank @Size(max=30) String unit, @NotBlank @Size(max=250) String location,
                       @NotBlank @Size(max=80) String area, @PositiveOrZero @Max(1000) double distance,
                       @NotNull Instant preparedAt, @NotNull Instant deadline, @NotBlank @Size(max=2800000) String image,
                       @NotNull @Size(max=250) String dietary, @NotNull @Size(max=250) String allergens) {}
    record UserView(String id, String name, String email, String role, String organization, String area) {
        static UserView of(Account a) { return new UserView(a.id,a.name,a.email,a.role,a.organization,a.area); }
    }
    record DonationView(String id, String name, String category, String description, int quantity, String unit,
                        String location, String area, double distance, Instant preparedAt, Instant deadline,
                        String image, String donor, String dietary, String allergens, String ownerId, boolean claimed, Instant createdAt) {
        static DonationView of(FoodDonation d) { return new DonationView(d.id,d.name,d.category,d.description,d.quantity,d.unit,
                d.location,d.area,d.distance,d.preparedAt,d.deadline,d.image,d.donor,d.dietary,d.allergens,d.owner.getId(),d.claimed,d.createdAt); }
    }
    record RequestView(String id, String donationId, String userId, String recipient, int stage, Instant createdAt,
                       List<Instant> timestamps, String volunteerId) {
        static RequestView of(Pickup p) { return new RequestView(p.id,p.donation.getId(),p.recipient.getId(),p.recipient.getName(),p.stage,
                p.createdAt,List.copyOf(p.timestamps),p.volunteer == null ? null : p.volunteer.getId()); }
    }
    record State(List<DonationView> donations, List<RequestView> requests, UserView user,
                 List<String> verified, List<Object> reports, List<Object> distributions) {}
}
