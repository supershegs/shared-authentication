## To share authentication between the service A and service B  
```
1. Set up a user model in the service A, including roles.  
2. Use JWT for authentication and store the secret key in the backend.  
3. When a user logs in, generate an access and refresh token.  
4. Save the tokens and user details (ID, username, email, role, etc.) in Redis.  
5. In the service B, create custom authentication:  
   - Extract the bearer token from the request.  
   - Check if it exists in Redis. If not, the token is invalid.  
   - If found, decode it using the shared secret key to verify its validity.  
   - If valid, return user details and allow the request to proceed.

```