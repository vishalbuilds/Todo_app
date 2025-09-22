# import secrets

# # Generate a cryptographically secure random key
# secret_key = secrets.token_urlsafe(32)  # 32 bytes ≈ 43 characters
# print(secret_key)





from jwt_handler import JWTHandler



ACCESS_SECRET_KEY = "xhS4oXm2YAmy77Fi0nHfJDlSLnNrCtRtr0dTZ4ZnjkM"
REFRESH_SECRET_KEY="ri3PML6FuYlIGeOGK5DL1FsIexoYOSuLoJlbh_B6POI"
token_obj=JWTHandler(REFRESH_SECRET_KEY,ACCESS_SECRET_KEY)



a=token_obj.verify_access_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMWY4ZWNhYmEtZmE5OS00YjViLWIyMjctYWRlMDUwZTQxYzU4IiwidXNlcm5hbWUiOiJ2aXNoYWxfc2luZ2giLCJqdGkiOiI2MGI0YTczNC1jYzE1LTQzNmYtOTRkMS02NWIxNDA0YTZiZmIiLCJleHAiOjE3NTg0NjU0MTJ9.xPGHgscFu9W1JPJNV00Az0rBUSIptOtjaTOLmbrxNSg",        
                        refresh=True        
                                )

print(a)