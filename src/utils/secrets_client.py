import secrets

# Generate a cryptographically secure random key
secret_key = secrets.token_urlsafe(32)  # 32 bytes ≈ 43 characters
print(secret_key)
