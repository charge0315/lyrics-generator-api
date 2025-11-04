# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of this project seriously. If you discover a security vulnerability, please follow these steps:

### Do NOT

- Open a public GitHub issue for security vulnerabilities
- Disclose the vulnerability publicly before it has been addressed

### Do

1. **Email the maintainer** at [your-email@example.com] with:
   - A description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Any suggested fixes (optional)

2. **Wait for acknowledgment** - We aim to respond within 48 hours

3. **Coordinate disclosure** - We will work with you to understand and address the issue

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Status Updates**: Regular updates on the progress
- **Resolution**: Depends on severity and complexity
- **Credit**: We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Best Practices

### For Contributors

- Never commit sensitive data (API keys, passwords, tokens)
- Use environment variables for configuration
- Follow secure coding practices
- Keep dependencies up to date
- Run security audits regularly:
  ```bash
  npm audit
  npm audit fix
  ```

### For Users

- Keep the application updated to the latest version
- Use strong, unique passwords
- Protect your API keys and credentials
- Review environment variable configurations
- Use HTTPS in production
- Enable appropriate authentication and authorization

## Known Security Considerations

### LyricsGenius API and Genius Credentials

This project uses the LyricsGenius library to fetch lyrics:
- Never share your Genius.com API token
- Store token in `.env` file (not committed to git)
- Regenerate tokens if they are exposed
- Respect Genius API rate limits to avoid IP blocking
- Review Genius terms of service for usage rights

### FastAPI Security Best Practices

- Implement proper CORS settings to prevent unauthorized cross-origin access
- Use HTTPS in production environments
- Validate and sanitize all input parameters
- Implement rate limiting to prevent API abuse
- Use authentication (Bearer tokens, API keys) if exposing the API publicly
- Implement request/response size limits
- Keep FastAPI and dependencies up to date

### ngrok Tunnel Security

- ngrok creates a public URL to access your local API
- Anyone with the ngrok URL can access your API
- Rotate ngrok authentication token regularly
- Monitor ngrok dashboard for unauthorized connections
- Consider using ngrok paid features for IP whitelisting
- Disable tunnel when not in use
- Use HTTPS-only ngrok tunnels for sensitive data

### Lyrics Caching

- The /lyrics/ directory may contain sensitive song/artist metadata
- Implement access controls if storing user-specific lyrics
- Clear cache when sharing the environment
- Be aware of copyright implications when storing/caching lyrics
- Implement data retention policies for cached content

### Local API Server Security

- API runs on localhost by default
- ngrok exposes it publicly; handle with care
- Implement request validation for song/artist names
- Add timeouts for API requests to prevent hanging connections
- Log access attempts for security monitoring
- Implement circuit breakers for external API calls

### Dependency Security

- Keep Python dependencies (FastAPI, uvicorn, lyricsgenius) updated
- Run `pip audit` regularly to check for known vulnerabilities
- Use virtual environments to isolate dependencies
- Review third-party library source code when possible
- Pin dependency versions in production to prevent unexpected changes

## Security Updates

Security updates will be released as soon as possible after a vulnerability is confirmed. Users will be notified through:

- GitHub Security Advisories
- Release notes
- Email notifications (for critical issues)

## Responsible Disclosure

We practice responsible disclosure:
- Vulnerabilities are fixed before public disclosure
- We provide credit to security researchers
- We coordinate with affected parties
- We release security advisories when appropriate

## Contact

For security concerns, please contact:
- Email: [your-email@example.com]
- GitHub: @charg

For general questions, please use GitHub issues instead.

---

Thank you for helping keep this project secure!
