package com.foodbridge;

import org.springframework.context.annotation.*;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.core.userdetails.*;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.csrf.*;
import org.springframework.security.web.context.*;
import org.springframework.security.web.authentication.session.ChangeSessionIdAuthenticationStrategy;

@Configuration
class SecurityConfig {
    @Bean PasswordEncoder passwordEncoder() { return new BCryptPasswordEncoder(12); }
    @Bean UserDetailsService userDetailsService(Accounts accounts) {
        return email -> accounts.findByEmail(email).map(a -> User.withUsername(a.email).password(a.passwordHash).authorities(a.role).build())
                .orElseThrow(() -> new UsernameNotFoundException("Invalid email or password."));
    }
    @Bean SecurityContextRepository securityContextRepository() { return new HttpSessionSecurityContextRepository(); }
    @Bean ChangeSessionIdAuthenticationStrategy sessionStrategy() { return new ChangeSessionIdAuthenticationStrategy(); }
    @Bean SecurityFilterChain security(HttpSecurity http, SecurityContextRepository repository) throws Exception {
        http.securityContext(c -> c.securityContextRepository(repository))
            .csrf(c -> c.csrfTokenRepository(new HttpSessionCsrfTokenRepository()).csrfTokenRequestHandler(new CsrfTokenRequestAttributeHandler()))
            .authorizeHttpRequests(a -> a
                .requestMatchers(HttpMethod.GET, "/api/state", "/api/auth/csrf", "/api/health").permitAll()
                .requestMatchers(HttpMethod.POST, "/api/auth/register", "/api/auth/login").permitAll()
                .anyRequest().authenticated())
            .exceptionHandling(e -> e
                .authenticationEntryPoint((req,res,ex) -> { res.setStatus(401); res.setContentType("application/json"); res.getWriter().write("{\"message\":\"Please sign in.\"}"); })
                .accessDeniedHandler((req,res,ex) -> { res.setStatus(403); res.setContentType("application/json"); res.getWriter().write("{\"message\":\"Access denied or security token expired. Refresh and try again.\"}"); }))
            .logout(l -> l.logoutUrl("/api/auth/logout").logoutSuccessHandler((req,res,a) -> res.setStatus(204)));
        return http.build();
    }
}
