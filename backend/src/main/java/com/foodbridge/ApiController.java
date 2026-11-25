package com.foodbridge;

import com.foodbridge.Contracts.*;
import com.foodbridge.Models.Account;
import jakarta.servlet.http.*;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.authentication.session.ChangeSessionIdAuthenticationStrategy;
import org.springframework.security.web.context.SecurityContextRepository;
import org.springframework.security.web.csrf.*;
import org.springframework.web.bind.annotation.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

@RestController @RequestMapping("/api")
class ApiController {
    private final FoodService service; private final Accounts accounts; private final PasswordEncoder passwords;
    private final SecurityContextRepository contexts; private final ChangeSessionIdAuthenticationStrategy sessions;
    ApiController(FoodService service, Accounts accounts, PasswordEncoder passwords, SecurityContextRepository contexts,
                  ChangeSessionIdAuthenticationStrategy sessions) {
        this.service=service; this.accounts=accounts; this.passwords=passwords; this.contexts=contexts; this.sessions=sessions;
    }
    private String email(Authentication auth) { return auth == null ? null : auth.getName(); }
    @GetMapping("/health") Map<String,String> health() { return Map.of("status","ok"); }
    @GetMapping("/auth/csrf") Map<String,String> csrf(CsrfToken token) { return Map.of("token",token.getToken(),"headerName",token.getHeaderName()); }
    @GetMapping("/state") State state(Authentication auth) { return service.state(email(auth)); }
    @PostMapping("/auth/register") @ResponseStatus(HttpStatus.CREATED)
    State register(@Valid @RequestBody Register input, HttpServletRequest req, HttpServletResponse res) {
        if (!Models.ROLES.contains(input.role())) throw FoodService.error(HttpStatus.BAD_REQUEST,"Choose a supported role. Administrator accounts cannot be registered publicly.");
        if (input.password().getBytes(StandardCharsets.UTF_8).length > 72) throw FoodService.error(HttpStatus.BAD_REQUEST,"Password must be at most 72 UTF-8 bytes.");
        String email=input.email().trim().toLowerCase(Locale.ROOT);
        if (accounts.findByEmail(email).isPresent()) throw FoodService.error(HttpStatus.CONFLICT,"An account with this email already exists.");
        Account a=new Account(); a.name=input.name().trim(); a.email=email; a.passwordHash=passwords.encode(input.password()); a.role=input.role();
        accounts.saveAndFlush(a); return establish(a,req,res);
    }
    @PostMapping("/auth/login") State login(@Valid @RequestBody Login input, HttpServletRequest req, HttpServletResponse res) {
        if (input.password().getBytes(StandardCharsets.UTF_8).length > 72) throw FoodService.error(HttpStatus.BAD_REQUEST,"Password must be at most 72 UTF-8 bytes.");
        Account a=accounts.findByEmail(input.email().trim().toLowerCase(Locale.ROOT)).orElse(null);
        // Always run the password hash, including for unknown accounts.
        String hash=a == null ? "$2a$12$QyDjS97W6GxXCs92VuQwNe/9nVeEavVCBr9MpFrRRMXkhQlJCjfzK" : a.passwordHash;
        boolean valid=passwords.matches(input.password(),hash);
        if (a == null || !valid) throw FoodService.error(HttpStatus.UNAUTHORIZED,"Invalid email or password.");
        return establish(a,req,res);
    }
    private State establish(Account a, HttpServletRequest req, HttpServletResponse res) {
        var auth=UsernamePasswordAuthenticationToken.authenticated(a.email,null,List.of(new SimpleGrantedAuthority(a.role)));
        sessions.onAuthentication(auth,req,res);
        var context=SecurityContextHolder.createEmptyContext(); context.setAuthentication(auth); SecurityContextHolder.setContext(context);
        contexts.saveContext(context,req,res); new HttpSessionCsrfTokenRepository().saveToken(null,req,res);
        return service.state(a.email);
    }
    @PatchMapping("/users/me") State profile(Authentication a, @Valid @RequestBody Profile input) { return service.profile(email(a),input); }
    @PostMapping("/donations") @ResponseStatus(HttpStatus.CREATED)
    State create(Authentication a, @Valid @RequestBody NewDonation input) { return service.create(email(a),input); }
    @DeleteMapping("/donations/{id}") State withdraw(Authentication a, @PathVariable String id) { return service.withdraw(email(a),id); }
    @PostMapping("/donations/{id}/claim") State claim(Authentication a, @PathVariable String id) { return service.claim(email(a),id); }
    @PostMapping("/pickups/{id}/accept") State accept(Authentication a, @PathVariable String id) { return service.accept(email(a),id); }
    @PostMapping("/pickups/{id}/advance") State advance(Authentication a, @PathVariable String id) { return service.advance(email(a),id); }
}
