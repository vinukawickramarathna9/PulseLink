const fs = require('fs');

function walk(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        file = dir + '/' + file;
        const stat = fs.statSync(file);
        if (stat && stat.isDirectory()) { 
            results = results.concat(walk(file));
        } else { 
            if (file.endsWith('.tsx') || file.endsWith('.ts')) {
                results.push(file);
            }
        }
    });
    return results;
}

const files = walk('G:/PulseLink/Frontend/src');
files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    let original = content;

    // We want to replace '$' formatting with 'Rs. '
    
    // Convert old literal replacements back if any LKR is present 
    // The previous request was for LKR but if user wanted Rs. instead, let's fix LKR too
    content = content.replace(/LKR\s+/g, 'Rs. ');

    // Replace '$' + (concatenation)
    content = content.replace(/'\$' \+/g, '\'Rs. \' +');
    content = content.replace(/"\$" \+/g, '\"Rs. \" +');
    // Replace `$${ -> `Rs. ${
    content = content.replace(/\`\$\$\{/g, '\`Rs. \${');
    content = content.replace(/\`\$\{/g, '\`Rs. \${');
    
    // Literal numbers like $45,680 -> Rs. 45,680
    content = content.replace(/\$([0-9]+(?:,[0-9]+)*(?:\.[0-9]+)?)/g, 'Rs. $1');
    content = content.replace(/>\$/g, '>Rs. ');
    content = content.replace(/'\$'/g, '\'Rs. \'');
    content = content.replace(/"\$"/g, '\"Rs. \"');
    content = content.replace(/Fee: \$/g, 'Fee: Rs. ');

    // For charts formatter ${value...} inside tooltip:
    content = content.replace(/}: \$\{/g, '}: Rs. \${');
    
    // Any formatting tick formatter using Rs. Rs.
    content = content.replace(/Rs\. Rs\./g, 'Rs. ');

    if (content !== original) {
        fs.writeFileSync(file, content);
        console.log('Fixed:', file);
    }
});