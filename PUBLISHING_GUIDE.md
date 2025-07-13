# 🍺 Publishing GetMeThatDawg to Homebrew

## ✅ Local Test Completed
The homebrew formula has been tested locally and works perfectly!

## 🚀 Publishing Steps

### Step 1: Create GitHub Repositories

You need to create **2 repositories** on GitHub:

#### 1. Main Project Repository
- **Name**: `getmethatdawg`
- **Description**: "Zero-config deployment for Python AI agents and web services"
- **Visibility**: Public
- **Initialize**: Don't initialize with README (we'll push our existing code)

#### 2. Homebrew Tap Repository  
- **Name**: `homebrew-getmethatdawg`
- **Description**: "Homebrew tap for GetMeThatDawg"
- **Visibility**: Public
- **Initialize**: Initialize with README

### Step 2: Push Main Project to GitHub

```bash
# In your current project directory
git init
git add .
git commit -m "feat: initial release of getmethatdawg v0.1.0"

# Add GitHub repository as origin (replace Dwij1704)
git remote add origin https://github.com/Dwij1704/getmethatdawg.git
git branch -M main
git push -u origin main
```

### Step 3: Create Release and Get SHA256

```bash
# Create a source tarball
make release

# This creates: dist/getmethatdawg-source.tar.gz
# Get the SHA256 for the homebrew formula
shasum -a 256 dist/getmethatdawg-source.tar.gz
```

OR use GitHub releases:
1. Go to your GitHub repository
2. Click "Create a new release"
3. Tag: `v0.1.0`
4. Title: `GetMeThatDawg v0.1.0`
5. Upload `dist/getmethatdawg-source.tar.gz`
6. GitHub will provide the SHA256

### Step 4: Update Homebrew Formula

Update `homebrew/getmethatdawg.rb` with real URLs:

```ruby
class Getmethatdawg < Formula
  desc "Zero-config deployment for Python AI agents and web services"
  homepage "https://github.com/Dwij1704/getmethatdawg"
  url "https://github.com/Dwij1704/getmethatdawg/releases/download/v0.1.0/getmethatdawg-source.tar.gz"
  sha256 "234b52193cbfc147b14f816c559f076440991776d1124293f0ca6d962795de62"
  license "MIT"
  
  # ... rest of formula stays the same
```

### Step 5: Set Up Homebrew Tap

```bash
# Clone your homebrew tap repository
git clone https://github.com/Dwij1704/homebrew-getmethatdawg.git
cd homebrew-getmethatdawg

# Create Formula directory
mkdir Formula

# Copy the updated formula
cp /path/to/your/project/homebrew/getmethatdawg.rb Formula/

# Commit and push
git add Formula/getmethatdawg.rb
git commit -m "feat: add getmethatdawg formula"
git push origin main
```

### Step 6: Test Public Installation

```bash
# Add your tap
brew tap Dwij1704/getmethatdawg

# Install your package
brew install getmethatdawg

# Test it works
getmethatdawg --version
```

### Step 7: Users Can Now Install

Once published, users can install with:

```bash
brew tap Dwij1704/getmethatdawg
brew install getmethatdawg
```

Or in one command:
```bash
brew install Dwij1704/getmethatdawg/getmethatdawg
```

## 📋 Pre-Publishing Checklist

- [ ] Main GitHub repository created
- [ ] Homebrew tap repository created  
- [ ] Project code pushed to main repo
- [ ] Release created with source tarball
- [ ] SHA256 obtained for the release
- [ ] Formula updated with correct URLs and SHA256
- [ ] Formula pushed to tap repository
- [ ] Installation tested from public tap

## 🎯 Quick Commands Summary

```bash
# Create repositories on GitHub first, then:

# 1. Push main project
git init && git add . && git commit -m "initial release"
git remote add origin https://github.com/Dwij1704/getmethatdawg.git
git push -u origin main

# 2. Create release
make release

# 3. Get SHA256  
shasum -a 256 dist/getmethatdawg-source.tar.gz

# 4. Update formula URLs and SHA256 in homebrew/getmethatdawg.rb

# 5. Set up tap
git clone https://github.com/Dwij1704/homebrew-getmethatdawg.git
cd homebrew-getmethatdawg
mkdir Formula
cp /path/to/homebrew/getmethatdawg.rb Formula/
git add . && git commit -m "add formula" && git push

# 6. Test installation
brew tap Dwij1704/getmethatdawg
brew install getmethatdawg
```

## 🚀 Ready to Publish!

Your homebrew formula is tested and ready. Follow the steps above to publish it to the world!

**Questions?** Just ask! I'm here to help you through each step. 