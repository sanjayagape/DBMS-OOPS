package com.foodbridge;

import com.foodbridge.Contracts.*;
import com.foodbridge.Models.*;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;
import java.time.Instant;
import java.util.*;

@Service @Transactional
class FoodService {
    private final Accounts accounts;
    private final Donations donations;
    private final Pickups pickups;
    FoodService(Accounts accounts, Donations donations, Pickups pickups) {
        this.accounts = accounts; this.donations = donations; this.pickups = pickups;
    }
    static ResponseStatusException error(HttpStatus status, String message) { return new ResponseStatusException(status,message); }
    Account account(String email) {
        if (email == null) throw error(HttpStatus.UNAUTHORIZED,"Please sign in.");
        return accounts.findByEmail(email).orElseThrow(() -> error(HttpStatus.UNAUTHORIZED,"Please sign in."));
    }
    static void require(boolean allowed, String message) { if (!allowed) throw error(HttpStatus.FORBIDDEN,message); }
    static void role(Account a, String... allowed) { require(Arrays.asList(allowed).contains(a.role),"Your account role cannot perform this action."); }

    @Transactional(readOnly = true)
    State state(String email) {
        Account user = email == null ? null : account(email);
        List<Pickup> visible = user == null ? List.of() : pickups.findAll().stream().filter(p ->
                user.role.equals("Administrator") || p.recipient.getId().equals(user.id) || p.donation.getOwner().getId().equals(user.id)
                || (p.volunteer != null && p.volunteer.getId().equals(user.id)) || (user.role.equals("Volunteer") && p.stage == 1)).toList();
        Set<String> involved = new HashSet<>(); visible.forEach(p -> involved.add(p.donation.getId()));
        List<DonationView> listings = donations.findAll().stream().map(d -> (FoodDonation) org.hibernate.Hibernate.unproxy(d)).filter(d ->
                (!d.claimed && d.deadline.isAfter(Instant.now())) || involved.contains(d.id)
                || (user != null && (d.owner.getId().equals(user.id) || user.role.equals("Administrator"))))
                .sorted(Comparator.comparing((FoodDonation d) -> d.createdAt).reversed()).map(DonationView::of).toList();
        return new State(listings,visible.stream().map(RequestView::of).toList(),user == null ? null : UserView.of(user),List.of(),List.of(),List.of());
    }
    State profile(String email, Profile input) {
        Account a = account(email); a.name = input.name().trim(); a.organization = input.organization().trim(); a.area = input.area().trim();
        return state(email);
    }
    State create(String email, NewDonation input) {
        Account a = account(email); role(a,"Food Donor");
        if (!Models.CATEGORIES.contains(input.category())) throw error(HttpStatus.BAD_REQUEST,"Choose a valid food category.");
        Instant now = Instant.now();
        if (!input.deadline().isAfter(now) || !input.deadline().isAfter(input.preparedAt()) || input.preparedAt().isAfter(now))
            throw error(HttpStatus.BAD_REQUEST,"Preparation must be in the past and pickup must be after preparation and in the future.");
        if (!Double.isFinite(input.distance())) throw error(HttpStatus.BAD_REQUEST,"Distance must be finite.");
        if (!(input.image().startsWith("https://") || input.image().matches("data:image/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+")))
            throw error(HttpStatus.BAD_REQUEST,"Use an HTTPS image URL or a JPEG, PNG, or WebP image.");
        FoodDonation d = new FoodDonation(); d.name=input.name().trim(); d.category=input.category(); d.description=input.description().trim();
        d.quantity=input.quantity(); d.unit=input.unit().trim(); d.location=input.location().trim(); d.area=input.area().trim();
        d.distance=input.distance(); d.preparedAt=input.preparedAt(); d.deadline=input.deadline(); d.image=input.image();
        d.dietary=input.dietary(); d.allergens=input.allergens(); d.owner=a; d.donor=a.organization.isBlank() ? a.name : a.organization;
        donations.saveAndFlush(d); return state(email);
    }
    State claim(String email, String id) {
        Account a = account(email); role(a,"Citizen","NGO");
        FoodDonation d = donations.lockById(id).orElseThrow(() -> error(HttpStatus.NOT_FOUND,"Donation not found."));
        require(!d.owner.getId().equals(a.id),"You cannot claim your own donation.");
        if (d.claimed || !d.deadline.isAfter(Instant.now())) throw error(HttpStatus.CONFLICT,"This donation has been claimed or its pickup window has closed.");
        d.claimed=true; Pickup p=new Pickup(); p.donation=d; p.recipient=a; p.timestamps.add(d.createdAt); p.timestamps.add(p.createdAt);
        pickups.saveAndFlush(p); return state(email);
    }
    State accept(String email, String id) {
        Account a=account(email); role(a,"Volunteer"); Pickup p=pickup(id);
        if (p.stage != 1) throw error(HttpStatus.CONFLICT,"This assignment is no longer available.");
        if (!p.donation.getDeadline().isAfter(Instant.now())) throw error(HttpStatus.CONFLICT,"The pickup window has closed.");
        p.volunteer=a; p.stage=2; p.timestamps.add(Instant.now()); return state(email);
    }
    State advance(String email, String id) {
        Account a=account(email); Pickup p=pickup(id);
        if (p.stage == 2) {
            require(p.volunteer != null && p.volunteer.getId().equals(a.id),"Only the assigned volunteer can confirm pickup.");
            if (!p.donation.getDeadline().isAfter(Instant.now())) throw error(HttpStatus.CONFLICT,"The pickup window has closed.");
        } else if (p.stage == 3) {
            require(p.recipient.getId().equals(a.id),"Only the recipient can confirm delivery.");
        } else throw error(HttpStatus.CONFLICT,p.stage == 4 ? "Delivery is already complete." : "A volunteer must accept the assignment first.");
        p.stage++; p.timestamps.add(Instant.now()); return state(email);
    }
    State withdraw(String email, String id) {
        Account a=account(email); FoodDonation d=donations.lockById(id).orElseThrow(() -> error(HttpStatus.NOT_FOUND,"Donation not found."));
        require(d.owner.getId().equals(a.id),"Only the donor can withdraw this listing.");
        if (d.claimed) throw error(HttpStatus.CONFLICT,"Claimed donations cannot be withdrawn.");
        donations.delete(d); donations.flush(); return state(email);
    }
    private Pickup pickup(String id) { return pickups.lockById(id).orElseThrow(() -> error(HttpStatus.NOT_FOUND,"Pickup not found.")); }
}
