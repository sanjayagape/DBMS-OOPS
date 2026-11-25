package com.foodbridge;

import com.fasterxml.jackson.databind.*;
import com.foodbridge.Models.*;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.*;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.*;
import static org.assertj.core.api.Assertions.*;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest @AutoConfigureMockMvc @ActiveProfiles("test")
class BackendIntegrationTest {
    @Autowired MockMvc mvc; @Autowired ObjectMapper json; @Autowired Accounts accounts;
    @Autowired Donations donations; @Autowired Pickups pickups; @Autowired FoodService service;
    private String unique() { return UUID.randomUUID().toString().substring(0,8); }
    private record Client(String email, MockHttpSession session) {}
    private Client register(String role) throws Exception {
        String email=unique()+"@example.com";
        MvcResult result=mvc.perform(post("/api/auth/register").with(csrf()).contentType("application/json")
                .content(json.writeValueAsString(Map.of("name","Test User","email",email,"password","StrongPass123!","role",role))))
                .andExpect(status().isCreated()).andReturn();
        assertThat(result.getResponse().getContentAsString()).doesNotContain("passwordHash","StrongPass123!");
        return new Client(email,(MockHttpSession) result.getRequest().getSession(false));
    }
    private String create(Client donor) throws Exception {
        Map<String,Object> body=new HashMap<>(Map.of("name","Fresh meals","category","Cooked meals","description","Freshly prepared meals",
                "quantity",10,"unit","meals","location","Community kitchen","area","Indiranagar","distance",1.5,
                "preparedAt",Instant.now().minusSeconds(60).toString(),"deadline",Instant.now().plusSeconds(3600).toString()));
        body.put("image","https://example.com/meal.jpg"); body.put("dietary","Vegetarian"); body.put("allergens","Milk");
        var result=mvc.perform(post("/api/donations").session(donor.session).with(csrf()).contentType("application/json")
                .content(json.writeValueAsString(body))).andExpect(status().isCreated()).andReturn();
        JsonNode state=json.readTree(result.getResponse().getContentAsString());
        String owner=accounts.findByEmail(donor.email).orElseThrow().id;
        for (JsonNode d:state.get("donations")) if (d.get("ownerId").asText().equals(owner)) return d.get("id").asText();
        throw new AssertionError("Created donation missing");
    }
    @Test void authenticationChecksCredentialsRolesAndCsrf() throws Exception {
        Client citizen=register("Citizen");
        assertThat(accounts.findByEmail(citizen.email).orElseThrow().passwordHash).startsWith("$2a$");
        mvc.perform(post("/api/auth/login").with(csrf()).contentType("application/json")
                .content(json.writeValueAsString(Map.of("email",citizen.email,"password","wrongpassword")))).andExpect(status().isUnauthorized());
        var login=mvc.perform(post("/api/auth/login").with(csrf()).contentType("application/json")
                .content(json.writeValueAsString(Map.of("email",citizen.email,"password","StrongPass123!"))))
                .andExpect(status().isOk()).andReturn();
        MockHttpSession session=(MockHttpSession) login.getRequest().getSession(false);
        mvc.perform(get("/api/state").session(session)).andExpect(jsonPath("$.user.role").value("Citizen"));
        mvc.perform(post("/api/auth/register").with(csrf()).contentType("application/json")
                .content(json.writeValueAsString(Map.of("name","Admin","email",unique()+"@example.com","password","StrongPass123!","role","Administrator"))))
                .andExpect(status().isBadRequest());
        mvc.perform(patch("/api/users/me").session(session).contentType("application/json")
                .content("{\"name\":\"Changed\",\"organization\":\"\",\"area\":\"HSR Layout\"}")).andExpect(status().isForbidden());
        mvc.perform(patch("/api/users/me").session(session).with(csrf()).contentType("application/json")
                .content("{\"name\":\"Changed\",\"organization\":\"\",\"area\":\"HSR Layout\",\"role\":\"Administrator\"}"))
                .andExpect(status().isBadRequest());
        mvc.perform(post("/api/auth/logout").session(session).with(csrf())).andExpect(status().isNoContent());
        assertThat(session.isInvalid()).isTrue();
        mvc.perform(get("/api/state")).andExpect(jsonPath("$.user").isEmpty());
    }
    @Test void lifecycleEnforcesOwnershipVisibilityAndTransitions() throws Exception {
        Client donor=register("Food Donor"), recipient=register("Citizen"), outsider=register("Citizen"), volunteer=register("Volunteer");
        String donation=create(donor);
        mvc.perform(delete("/api/donations/"+donation).session(outsider.session).with(csrf())).andExpect(status().isForbidden());
        var claimed=mvc.perform(post("/api/donations/"+donation+"/claim").session(recipient.session).with(csrf()))
                .andExpect(status().isOk()).andReturn();
        String pickup=json.readTree(claimed.getResponse().getContentAsString()).get("requests").get(0).get("id").asText();
        mvc.perform(post("/api/donations/"+donation+"/claim").session(outsider.session).with(csrf())).andExpect(status().isConflict());
        mvc.perform(delete("/api/donations/"+donation).session(donor.session).with(csrf())).andExpect(status().isConflict());
        mvc.perform(get("/api/state").session(outsider.session)).andExpect(jsonPath("$.requests").isEmpty());
        mvc.perform(post("/api/pickups/"+pickup+"/advance").session(recipient.session).with(csrf())).andExpect(status().isConflict());
        mvc.perform(post("/api/pickups/"+pickup+"/accept").session(volunteer.session).with(csrf())).andExpect(status().isOk());
        mvc.perform(post("/api/pickups/"+pickup+"/advance").session(donor.session).with(csrf())).andExpect(status().isForbidden());
        mvc.perform(post("/api/pickups/"+pickup+"/advance").session(volunteer.session).with(csrf())).andExpect(status().isOk());
        mvc.perform(post("/api/pickups/"+pickup+"/advance").session(volunteer.session).with(csrf())).andExpect(status().isForbidden());
        var delivered=mvc.perform(post("/api/pickups/"+pickup+"/advance").session(recipient.session).with(csrf()))
                .andExpect(status().isOk()).andReturn();
        var request=json.readTree(delivered.getResponse().getContentAsString()).get("requests").get(0);
        assertThat(request.get("stage").asInt()).isEqualTo(4); assertThat(request.get("timestamps").size()).isEqualTo(5);
        mvc.perform(post("/api/pickups/"+pickup+"/advance").session(recipient.session).with(csrf())).andExpect(status().isConflict());
    }
    @Test void concurrentClaimsHaveOnlyOneWinner() throws Exception {
        Client donor=register("Food Donor"), first=register("Citizen"), second=register("NGO"); String id=create(donor);
        ExecutorService pool=Executors.newFixedThreadPool(2); CountDownLatch start=new CountDownLatch(1);
        try {
            List<Future<Boolean>> attempts=new ArrayList<>();
            for (Client c:List.of(first,second)) attempts.add(pool.submit(() -> { start.await(); try { service.claim(c.email,id); return true; }
                catch (org.springframework.web.server.ResponseStatusException ex) { assertThat(ex.getStatusCode().value()).isEqualTo(409); return false; } }));
            start.countDown(); int winners=0; for (Future<Boolean> attempt:attempts) if (attempt.get(15,TimeUnit.SECONDS)) winners++;
            assertThat(winners).isEqualTo(1);
        } finally { pool.shutdownNow(); }
    }
    @Test void expirationAndInvalidDonationAreRejected() throws Exception {
        Client donor=register("Food Donor"), citizen=register("Citizen"); String id=create(donor);
        FoodDonation d=donations.findById(id).orElseThrow(); d.deadline=Instant.now().minusSeconds(1); donations.saveAndFlush(d);
        mvc.perform(post("/api/donations/"+id+"/claim").session(citizen.session).with(csrf())).andExpect(status().isConflict());
        mvc.perform(post("/api/donations").session(donor.session).with(csrf()).contentType("application/json").content("{}"))
                .andExpect(status().isBadRequest());
    }
    @Test void browserCsrfTokenWorksAndRotatesAfterAuthentication() throws Exception {
        var initial=mvc.perform(get("/api/auth/csrf")).andExpect(status().isOk()).andReturn();
        MockHttpSession session=(MockHttpSession) initial.getRequest().getSession(false);
        String token=json.readTree(initial.getResponse().getContentAsString()).get("token").asText();
        mvc.perform(post("/api/auth/register").session(session).header("X-CSRF-TOKEN",token).contentType("application/json")
                .content(json.writeValueAsString(Map.of("name","Browser User","email",unique()+"@example.com","password","StrongPass123!","role","Citizen"))))
                .andExpect(status().isCreated());
        var refreshed=mvc.perform(get("/api/auth/csrf").session(session)).andReturn();
        String next=json.readTree(refreshed.getResponse().getContentAsString()).get("token").asText();
        assertThat(next).isNotEqualTo(token);
        mvc.perform(patch("/api/users/me").session(session).header("X-CSRF-TOKEN",next).contentType("application/json")
                .content("{\"name\":\"Browser User\",\"organization\":\"\",\"area\":\"HSR Layout\"}"))
                .andExpect(status().isOk());
    }
}
