# Security Policy

## Supported Versions

We currently support the following versions of SABRINA with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in SABRINA, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email the maintainers directly or use GitHub's private vulnerability reporting
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond to security reports within 48 hours and work to address critical vulnerabilities promptly.

## Security Best Practices

When using SABRINA:

- **API Keys**: Never commit API keys to the repository. Use environment variables.
- **Secret Key**: Use a strong, randomly generated secret key for Flask sessions.
- **Dependencies**: Keep dependencies up to date to avoid known vulnerabilities.
- **HTTPS**: Use HTTPS in production environments.
- **Input Validation**: Always validate user input on both client and server side.

## Known Security Considerations

- The application uses Flask sessions - ensure `SECRET_KEY` is kept secure
- API keys should be stored as environment variables, not in code
- User input is sanitized, but always validate on the backend
- The application is designed for educational use in controlled environments

## Disclosure Policy

- Vulnerabilities will be disclosed after a fix is available
- We will credit security researchers who responsibly report vulnerabilities
- Critical vulnerabilities will be patched as quickly as possible

Thank you for helping keep SABRINA secure!

