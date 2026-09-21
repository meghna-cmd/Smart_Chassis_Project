# Security and Access Control

This prototype includes basic input validation in `api.py`:
- Request size limits
- Numeric finite-value validation
- HTTP 400 responses for invalid data

Before production deployment, add:
- Authentication and authorization
- HTTPS/TLS
- Rate limiting
- Secrets stored outside source code
- Audit logging
- Dependency and container vulnerability scanning
- Role-based access control
