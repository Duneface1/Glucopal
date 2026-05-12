package com.diabetesapp.controller;

import com.diabetesapp.dto.UserDto;
import com.diabetesapp.service.UserService;
import com.diabetesapp.service.ChatService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;
    private final ChatService chatService;

    @GetMapping("/{id}")
    public ResponseEntity<UserDto.Response> getProfile(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getProfile(id));
    }

    @PutMapping("/{id}/profile")
    public ResponseEntity<UserDto.Response> updateProfile(
            @PathVariable Long id,
            @Valid @RequestBody UserDto.UpdateRequest request) {
        return ResponseEntity.ok(userService.updateProfile(id, request));
    }

    @PostMapping("/{id}/chat")
    public ResponseEntity<UserDto.ChatResponse> chat(
            @PathVariable Long id,
            @Valid @RequestBody UserDto.ChatRequest request) {
        return ResponseEntity.ok(chatService.chat(request.getMessage()));
    }
}