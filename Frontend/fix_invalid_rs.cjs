const fs = require('fs');
const path = require('path');

const directory = 'Frontend/src';

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const fileDir = dir + '/' + file;
    const stat = fs.statSync(fileDir);
    if (stat && stat.isDirectory()) {
      results = results.concat(walk(fileDir));
    } else {
      if (fileDir.endsWith('.tsx') || fileDir.endsWith('.ts')) {
        results.push(fileDir);
      }
    }
  });
  return results;
}

const files = walk(directory);
let updatedFiles = 0;

files.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  let original = content;

  // Fix API fetch URLs
  content = content.replace(/`Rs\. \$\{API_BASE_URL\}/g, '`${API_BASE_URL}');
  
  // Fix React elements / string templates that shouldn't be Rs
  content = content.replace(/`Rs\. \$\{(value|percent) \*\ 100\}(.*?)[%]`/, '`${$1 * 100}$2%`');
  content = content.replace(/`Rs\. \$\{(.*?)\}%\`/g, '`${$1}%`');
  content = content.replace(/`Rs\. \$\{(value)\}\/5\.0\`/g, '`${$1}/5.0`');
  content = content.replace(/`Rs\. \$\{(.*?)\.length\}(.*?)`/g, '`${$1.length}$2`');
  content = content.replace(/`Rs\. \$\{patient\.name\}(.*?)`/g, '`${patient.name}$2`');
  content = content.replace(/`Rs\. \$\{import\.meta\.env\.(.*?)\}(.*?)`/g, '`${import.meta.env.$1}$2`');
  content = content.replace(/`Rs\. \$\{file\.progress\}%`/g, '`${file.progress}%`');

  if (content !== original) {
    fs.writeFileSync(file, content, 'utf8');
    updatedFiles++;
    console.log(`Fixed formatting in ${file}`);
  }
});

console.log(`Reverted invalid Rs. replacements in ${updatedFiles} files.`);
