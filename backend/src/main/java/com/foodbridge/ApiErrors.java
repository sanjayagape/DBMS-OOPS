package com.foodbridge;

import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.*;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.converter.HttpMessageNotReadableException;
import java.util.Map;
import java.util.stream.Collectors;

@RestControllerAdvice
class ApiErrors {
    @ExceptionHandler(ResponseStatusException.class)
    ResponseEntity<?> status(ResponseStatusException ex) { return ResponseEntity.status(ex.getStatusCode()).body(Map.of("message",ex.getReason() == null ? "Request failed." : ex.getReason())); }
    @ExceptionHandler(MethodArgumentNotValidException.class)
    ResponseEntity<?> validation(MethodArgumentNotValidException ex) {
        return ResponseEntity.badRequest().body(Map.of("message","Please check the submitted fields.","errors",
                ex.getBindingResult().getFieldErrors().stream().collect(Collectors.toMap(e -> e.getField(),e -> e.getDefaultMessage(),(a,b) -> a))));
    }
    @ExceptionHandler(HttpMessageNotReadableException.class)
    ResponseEntity<?> malformed() { return ResponseEntity.badRequest().body(Map.of("message","Invalid request body or unsupported fields.")); }
    @ExceptionHandler(DataIntegrityViolationException.class)
    ResponseEntity<?> conflict() { return ResponseEntity.status(409).body(Map.of("message","This email or reservation already exists.")); }
}
