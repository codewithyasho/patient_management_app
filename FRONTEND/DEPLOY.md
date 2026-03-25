# GitHub Pages Deployment Guide 🚀

## Quick Deploy to GitHub Pages

### Step 1: Create GitHub Repository

1. Go to <https://github.com/new>
2. Enter repository name: `patient-management-frontend`
3. Choose "Public" (required for GitHub Pages)
4. Click "Create repository"

### Step 2: Upload Frontend Files

#### Option A: Using Git (Recommended)

```bash
# Clone the repository to your local machine
git clone https://github.com/YOUR_USERNAME/patient-management-frontend.git
cd patient-management-frontend

# Copy FRONTEND contents into this folder
# (Copy all files from your FRONTEND folder here)

# Stage and commit changes
git add .
git commit -m "Initial commit: Patient Management Frontend"
git push origin main
```

#### Option B: Upload via GitHub Web UI

1. Go to your repository
2. Click "Add file" → "Upload files"
3. Drag and drop all FRONTEND files
4. Write commit message
5. Click "Commit changes"

### Step 3: Enable GitHub Pages

1. Go to Repository Settings (click "Settings" tab)
2. Scroll down to "GitHub Pages" section
3. Under "Branch":
   - Select: `main` (or `master`)
   - Select: `/ (root)`
4. Click "Save"
5. Wait 1-2 minutes for deployment

### Step 4: Access Your Frontend

Your site will be available at:

- **Default**: `https://YOUR_USERNAME.github.io/patient-management-frontend`
- **Specific**: `https://YOUR_USERNAME.github.io/patient-management-frontend/index.html`

## Custom Domain (Optional)

1. In Settings → Pages
2. Enter your custom domain in "Custom domain"
3. Click "Save"
4. Update DNS records at your domain registrar (usually):

   ```
   CNAME → your-domain.com → YOUR_USERNAME.github.io
   ```

5. Wait for DNS propagation (5-30 minutes)

## Verify Deployment

1. Visit your GitHub Pages URL
2. Check browser console for errors (F12)
3. Try adding a test patient
4. Verify all CRUD operations work

## Troubleshooting GitHub Pages

### Site Not Showing Up

- Wait 1-2 minutes after enabling
- Refresh page (Ctrl+Shift+R)
- Check "GitHub Pages" settings
- Verify files are in root directory

### CSS/JS Not Loading

- Check file paths in HTML
- Ensure no trailing slashes
- Clear browser cache
- Hard refresh (Ctrl+Shift+R)

### API Not Working

- Verify `API_BASE_URL` in `main.js`
- Check CORS settings on backend
- Test backend API directly
- Check browser console for errors

## Keep Frontend Updated

After making changes locally:

```bash
cd patient-management-frontend
git status                    # See changes
git add .                     # Stage all changes
git commit -m "Update: ..."   # Commit with message
git push origin main          # Deploy to GitHub Pages
```

Changes deploy automatically within 1-2 minutes!

## Project Structure for Deployment

Ensure your repository root looks like this:

```
patient-management-frontend/
├── index.html
├── main.js
├── styles.css
├── README.md                 # (Optional but recommended)
├── DEPLOY.md                 # (This file, optional)
└── LICENSE                   # (Optional)
```

## Best Practices

✅ **DO:**

- Use semantic commit messages
- Keep sensitive data out of code
- Test locally before pushing
- Document any API changes
- Update README with instructions

❌ **DON'T:**

- Include node_modules or build files
- Commit API keys or secrets
- Delete important branches
- Deploy untested code
- Use relative paths without consideration

## Advanced: Custom Build Process

If you want to minify or optimize files:

1. Create a `build` script locally
2. Generate optimized files
3. Commit only the optimized `index.html`, `main.js`, `styles.css`
4. Deploy as usual

## SSL/HTTPS

GitHub Pages automatically provides:

- ✅ Free HTTPS certificate
- ✅ Auto-renewal
- ✅ Force HTTPS on custom domains

## Performance Tips

1. **Lazy Loading**: Consider lazy-loading images if added
2. **Caching**: GitHub Pages handles caching automatically
3. **CDN**: Tailwind CSS is already from CDN
4. **Minification**: Optional but recommended for production

## Statistics After Deploy

Check your GitHub Pages site stats:

1. Settings → Pages → scroll to "GitHub Pages analytics"
2. View in Insights tab

## Need Help?

- GitHub Pages Docs: <https://pages.github.com/>
- Troubleshooting: <https://docs.github.com/en/pages>
- Frontend README: See README.md in this folder

---

**You're all set! Your Patient Management Frontend is live! 🎉**
