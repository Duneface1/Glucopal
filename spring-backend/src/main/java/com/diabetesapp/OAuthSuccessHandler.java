package com.diabetesapp;

import com.diabetesapp.model.User;
import com.diabetesapp.repository.UserRepository;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
@RequiredArgsConstructor
public class OAuthSuccessHandler implements AuthenticationSuccessHandler {

    private final UserRepository userRepo;
    private final JwtUtil jwtUtil;

    @Value("${app.frontend-url:http://localhost:5173}")
    private String frontendUrl;

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request,
                                        HttpServletResponse response,
                                        Authentication authentication) throws IOException {

        OAuth2User oauthUser = (OAuth2User) authentication.getPrincipal();

        String email = oauthUser.getAttribute("email");
        String name  = oauthUser.getAttribute("name");

        if (email == null) {
            response.sendRedirect(frontendUrl + "/oauth-callback?token=" + accessToken + "&redirect=" + redirectPath);

            return;
        }

        User user = userRepo.findByEmail(email).orElseGet(() -> {
            User newUser = new User();
            newUser.setEmail(email);
            newUser.setName(name != null ? name : email);
            newUser.setPasswordHash(null);
            newUser.setAuthProvider("google");
            return userRepo.save(newUser);
        });

        // Generate JWT
        String accessToken = jwtUtil.generateToken(user.getId(), user.getEmail());

        boolean isNewUser = user.getDiabetesType() == null && user.getPhone() == null;
        String redirectPath = isNewUser ? "/onboarding" : "/dashboard";

        String frontendUrl = allowedOriginsRaw.split(",")[0].trim();
        response.sendRedirect(frontendUrl + "/oauth-callback?token=" + accessToken + "&redirect=" + redirectPath);
    }
}