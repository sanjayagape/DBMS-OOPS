package com.foodbridge;

import com.foodbridge.Models.*;
import jakarta.persistence.LockModeType;
import org.springframework.data.jpa.repository.*;
import java.util.Optional;

interface Accounts extends JpaRepository<Account, String> {
    Optional<Account> findByEmail(String email);
}
interface Donations extends JpaRepository<FoodDonation, String> {
    @Lock(LockModeType.PESSIMISTIC_WRITE) @Query("select d from FoodDonation d where d.id = :id")
    Optional<FoodDonation> lockById(String id);
}
interface Pickups extends JpaRepository<Pickup, String> {
    @Lock(LockModeType.PESSIMISTIC_WRITE) @Query("select p from Pickup p where p.id = :id")
    Optional<Pickup> lockById(String id);
}
