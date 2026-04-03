const fs = require('fs');
const path = require('path');

const files = fs.readdirSync('.').filter(f => f.endsWith('.html'));

files.forEach(file => {
    let content = fs.readFileSync(file, 'utf-8');
    
    // Replace Tailwind CDN and config
    content = content.replace(/<script src="https:\/\/cdn\.tailwindcss\.com"><\/script>\s*<script>[\s\S]*?tailwind\.config[\s\S]*?<\/script>/g, '<link rel="stylesheet" href="style.css">');
    
    // Add referrer meta tag if not exists
    if (!content.includes('<meta name="referrer"')) {
        content = content.replace(/<head>/, '<head>\n    <meta name="referrer" content="no-referrer-when-downgrade">');
    }
    
    fs.writeFileSync(file, content);
    console.log(`Updated ${file}`);
});
