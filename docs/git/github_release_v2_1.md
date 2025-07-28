# 📦 Ash Dashboard GitHub Release Guide v2.1

**Updated for Submodule Structure & Dedicated Server**  
**Repository:** https://github.com/the-alphabet-cartel/ash-dash

## 📋 Release Overview

This guide covers the release management process for Ash Dashboard within the new submodule ecosystem structure. The dashboard follows semantic versioning and integrates with the overall Ash ecosystem release cycle.

### 🏗️ Release Structure

**Individual Component Releases:**
- **ash-dash:** Dashboard-specific features and fixes
- **Semantic Versioning:** Major.Minor.Patch (e.g., v2.1.3)
- **Release Branches:** `release/v2.1.x` for maintenance releases
- **Main Branch:** Always deployable production code

**Ecosystem Integration:**
- **Main Ash Repository:** Coordinates all component versions
- **Submodule Updates:** Automatic submodule reference updates
- **Synchronized Deployments:** Coordinated releases across components

## 🔄 Release Types

### 1. Patch Releases (v2.1.x)

**Purpose:** Bug fixes, security updates, minor improvements  
**Frequency:** As needed  
**Approval:** Lead Developer or Team Lead

**Process:**
```bash
# Create patch branch from main
git checkout main
git pull origin main
git checkout -b release/v2.1.1

# Apply bug fixes
git cherry-pick <bug-fix-commits>

# Update version
npm version patch

# Update CHANGELOG.md
# Add patch notes and bug fixes

# Create pull request
gh pr create --title "Release v2.1.1" --body "Patch release with bug fixes"

# After approval and merge
git checkout main
git pull origin main
git tag v2.1.1
git push origin main --tags
```

### 2. Minor Releases (v2.x.0)

**Purpose:** New features, API additions, significant improvements  
**Frequency:** Monthly or quarterly  
**Approval:** Team consensus and testing validation

**Process:**
```bash
# Create minor release branch
git checkout main
git pull origin main
git checkout -b release/v2.2.0

# Finalize features from develop branch
git merge develop

# Update version
npm version minor

# Run comprehensive testing
npm run test:comprehensive
npm run test:integration
npm run test:security

# Update documentation
# Update API documentation
# Update deployment guides
# Update troubleshooting guides

# Update CHANGELOG.md with new features

# Create pull request with comprehensive testing results
gh pr create --title "Release v2.2.0" --body-file release-notes-v2.2.0.md

# After approval, merge and tag
git checkout main
git pull origin main
git tag v2.2.0
git push origin main --tags
```

### 3. Major Releases (vX.0.0)

**Purpose:** Breaking changes, architecture updates, major feature overhauls  
**Frequency:** Annually or bi-annually  
**Approval:** Full team review and extended testing period

**Process:**
```bash
# Create major release branch
git checkout main
git pull origin main
git checkout -b release/v3.0.0

# Merge breaking changes from develop
git merge develop

# Update version
npm version major

# Extensive testing period (2-4 weeks)
npm run test:comprehensive
npm run test:load
npm run test:security
npm run test:compatibility

# Update all documentation
# Migration guides for breaking changes
# Updated API documentation
# New installation procedures

# Beta release for community testing
git tag v3.0.0-beta.1
git push origin --tags

# After beta testing and fixes
git tag v3.0.0
git push origin main --tags
```

## 📝 Release Documentation

### CHANGELOG.md Format

```markdown
# Changelog

All notable changes to Ash Dashboard will be documented in this file.

## [2.1.1] - 2025-01-28

### 🐛 Bug Fixes
- Fixed memory leak in real-time crisis monitoring
- Resolved authentication timeout issues
- Corrected dashboard refresh rate calculations

### 🔒 Security
- Updated dependencies with security vulnerabilities
- Enhanced input validation for API endpoints

### 📊 Performance
- Optimized database queries for analytics dashboard
- Improved caching strategy for team management data

## [2.1.0] - 2025-01-15

### 🚀 New Features
- **Advanced Analytics:** Enhanced crisis pattern recognition
- **Team Scheduling:** Automated shift management for response teams
- **Mobile Responsive:** Improved mobile dashboard experience
- **Export Capabilities:** PDF and CSV export for reports

### 🔧 Improvements
- Reduced dashboard load time by 40%
- Enhanced real-time update performance
- Improved error handling and user feedback
- Updated UI/UX for better accessibility

### 🔄 Changes
- Updated service integration endpoints for new server structure
- Migrated to new authentication system
- Consolidated configuration management

### 🐛 Bug Fixes
- Fixed timezone handling in scheduling system
- Resolved WebSocket connection stability issues
- Corrected permission handling for team roles

### 📚 Documentation
- Updated deployment guide for dedicated server
- Added troubleshooting guide for common issues
- Enhanced API documentation with examples

### 🔒 Security
- Implemented rate limiting for API endpoints
- Enhanced audit logging for team actions
- Updated Discord OAuth2 integration security

### ⚠️ Breaking Changes
- None (backward compatible)

### 🔗 Dependencies
- Updated to Node.js 20 LTS
- Upgraded Vue.js to v3.4
- Updated security dependencies

### 🧪 Testing
- Added comprehensive integration tests
- Enhanced security testing suite
- Improved test coverage to 95%
```

### Release Notes Template

```markdown
# 🚀 Ash Dashboard v2.1.1 Release

**Release Date:** January 28, 2025  
**Type:** Patch Release  
**Compatibility:** Fully backward compatible with v2.1.0

## 📊 Release Highlights

### 🐛 Critical Bug Fixes
- **Memory Leak Resolution:** Fixed significant memory leak in real-time monitoring that could cause dashboard slowdown
- **Authentication Stability:** Resolved timeout issues affecting team member access
- **Data Accuracy:** Corrected calculation errors in analytics dashboard

### 🔒 Security Enhancements
- Updated 12 dependencies with known security vulnerabilities
- Enhanced input validation preventing potential XSS attacks
- Strengthened API endpoint security

### 📈 Performance Improvements
- 25% reduction in memory usage during peak load
- Improved database query performance for large datasets
- Enhanced caching efficiency for frequently accessed data

## 🔧 Technical Details

### Dependencies Updated
- `express`: 4.18.2 → 4.18.3 (security patches)
- `lodash`: 4.17.20 → 4.17.21 (vulnerability fix)
- `axios`: 1.6.0 → 1.6.2 (security update)

### Database Migrations
- No database changes required
- Backward compatible with existing data

### Configuration Changes
- No configuration changes required
- All existing `.env` files remain valid

## 🚀 Deployment Instructions

### Automatic Deployment (Recommended)
```bash
# Update dashboard via ecosystem
cd /opt/ash
git pull origin main
git submodule update --recursive
docker-compose restart ash-dash
```

### Manual Deployment
```bash
# Update dashboard directly
cd /opt/ash/ash-dash
git pull origin main
docker-compose up -d --build
```

### Verification
```bash
# Verify deployment
curl https://10.20.30.253:8883/health
curl https://10.20.30.253:8883/api/version
```

## 🧪 Testing Results

### Automated Testing
- **Unit Tests:** 1,247 tests passed ✅
- **Integration Tests:** 89 tests passed ✅
- **Security Tests:** 45 tests passed ✅
- **Performance Tests:** All benchmarks met ✅

### Load Testing
- **Concurrent Users:** Tested up to 500 concurrent users
- **Response Time:** < 200ms for 95% of requests
- **Memory Usage:** Stable under extended load

## 🔍 Known Issues

### Minor Issues (Non-blocking)
- Dashboard theme switching may require page refresh in some browsers
- Export functionality may timeout for very large datasets (>50k records)

### Workarounds Available
- Use browser refresh after theme changes
- Use date filters to reduce export dataset size

## 📞 Support Information

### Immediate Support
- **Discord:** https://discord.gg/alphabetcartel (#tech-support)
- **GitHub Issues:** https://github.com/the-alphabet-cartel/ash-dash/issues

### Documentation
- **[Deployment Guide](docs/deployment_v2_1.md)**
- **[Troubleshooting Guide](docs/tech/troubleshooting_v2_1.md)**
- **[API Documentation](docs/tech/api_v2_1.md)**

## 🔄 Rollback Instructions

If issues are encountered, rollback to v2.1.0:

```bash
cd /opt/ash/ash-dash
git checkout v2.1.0
docker-compose up -d --build
```

## 📈 What's Next

### Upcoming in v2.2.0
- Enhanced mobile responsive design
- Advanced crisis prediction algorithms
- Team performance analytics dashboard
- Integration with external monitoring tools

### Release Timeline
- **v2.2.0 Beta:** February 15, 2025
- **v2.2.0 Release:** March 1, 2025

---

**Thank you to all contributors and the community for making this release possible!**

🌈 **The Alphabet Cartel** | **Discord:** https://discord.gg/alphabetcartel | **Website:** http://alphabetcartel.org
```

## 🚀 Release Automation

### GitHub Actions Workflow

```yaml
# .github/workflows/release.yml
name: Release Dashboard

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        
    - name: Install dependencies
      run: npm ci
      
    - name: Run tests
      run: npm run test:comprehensive
      
    - name: Build production
      run: npm run build:prod
      
    - name: Create release notes
      run: |
        node scripts/generate-release-notes.js > release-notes.md
        
    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        body_path: release-notes.md
        draft: false
        prerelease: false
        
    - name: Build Docker image
      run: |
        docker build -t ash-dash:${{ github.ref_name }} .
        docker tag ash-dash:${{ github.ref_name }} ash-dash:latest
        
    - name: Update ecosystem repository
      run: |
        # Trigger ecosystem update
        curl -X POST \
          -H "Authorization: token ${{ secrets.ECOSYSTEM_TOKEN }}" \
          -H "Accept: application/vnd.github.v3+json" \
          https://api.github.com/repos/the-alphabet-cartel/ash/dispatches \
          -d '{"event_type":"dashboard-release","client_payload":{"version":"${{ github.ref_name }}"}}'
```

### Release Checklist

**Pre-Release Checklist:**
- [ ] All tests passing (unit, integration, security)
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Security review completed
- [ ] Breaking changes documented
- [ ] Migration scripts tested (if applicable)

**Release Process Checklist:**
- [ ] Version bumped correctly
- [ ] Git tag created and pushed
- [ ] GitHub release created with notes
- [ ] Docker image built and tagged
- [ ] Deployment tested on staging
- [ ] Production deployment scheduled
- [ ] Team notified of release

**Post-Release Checklist:**
- [ ] Production deployment verified
- [ ] Health checks passing
- [ ] Integration tests passing
- [ ] Performance metrics normal
- [ ] Team trained on new features
- [ ] Documentation links updated
- [ ] Community announcement posted

## 🔗 Integration with Ecosystem

### Submodule Update Process

When ash-dash releases a new version, the main Ash repository must be updated:

```bash
# In main ash repository
cd /opt/ash
git submodule update --remote ash-dash
git add ash-dash
git commit -m "Update ash-dash to v2.1.1"
git push origin main

# Tag ecosystem release if needed
git tag ecosystem-v2.1.1
git push origin --tags
```

### Coordinated Releases

For major releases, coordinate with other components:

```bash
# Release coordination meeting agenda:
# 1. Review all component versions
# 2. Identify integration requirements
# 3. Schedule coordinated release timeline
# 4. Plan rollback procedures
# 5. Assign testing responsibilities
```

## 📞 Release Support

### Release Manager Responsibilities
- **Version Management:** Ensuring proper semantic versioning
- **Quality Assurance:** Coordinating testing and validation
- **Documentation:** Maintaining release documentation
- **Communication:** Announcing releases to team and community
- **Issue Tracking:** Managing post-release issues and patches

### Emergency Release Process

For critical security or production issues:

```bash
# Emergency hotfix process
git checkout main
git checkout -b hotfix/security-patch
# Apply minimal fix
git commit -m "Security hotfix: [CVE-XXXX]"
npm version patch
git tag v2.1.2
git push origin --tags

# Immediate deployment
ssh server "cd /opt/ash/ash-dash && git pull && docker-compose restart ash-dash"
```

---

**This release guide ensures consistent, reliable, and well-documented releases for the Ash Dashboard component of the crisis detection ecosystem.**