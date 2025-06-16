#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import https from 'https';
import http from 'http';
import yaml from 'js-yaml';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const NAMES_DIR = path.join(__dirname, '..', 'src', 'content', 'names');
const TIMEOUT = 5000; // 5 seconds timeout

function makeRequest(url, useHttps = true) {
  return new Promise((resolve, reject) => {
    const client = useHttps ? https : http;
    const parsedUrl = new URL(url);
    
    const options = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || (useHttps ? 443 : 80),
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'HEAD',
      timeout: TIMEOUT,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    };

    const req = client.request(options, (res) => {
      resolve({
        statusCode: res.statusCode,
        success: res.statusCode >= 200 && res.statusCode < 400
      });
    });

    req.on('error', (err) => {
      reject(err);
    });

    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });

    req.end();
  });
}

async function checkDomain(domain, explicitUrl = null) {
  const urlsToTry = [];
  
  if (explicitUrl) {
    urlsToTry.push(explicitUrl);
  } else {
    urlsToTry.push(`https://${domain}`);
    urlsToTry.push(`http://${domain}`);
  }

  for (const url of urlsToTry) {
    try {
      const isHttps = url.startsWith('https://');
      const result = await makeRequest(url, isHttps);
      
      if (result.success) {
        return { success: true, url, statusCode: result.statusCode };
      }
    } catch (error) {
      // Continue to next URL
      continue;
    }
  }
  
  return { success: false, url: null, statusCode: null };
}

async function processYamlFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const data = yaml.load(content);
    
    if (!data || !data.domain) {
      console.log(`SKIP: ${path.basename(filePath)} - No domain field`);
      return { updated: false };
    }

    const domain = data.domain;
    const explicitUrl = data.url || null;
    
    console.log(`CHECKING: ${domain}${explicitUrl ? ` (explicit URL: ${explicitUrl})` : ''}`);
    
    const result = await checkDomain(domain, explicitUrl);
    
    if (result.success) {
      console.log(`✓ FOUND: ${domain} at ${result.url} (${result.statusCode})`);
      
      // Remove invalid flag if it was previously set
      if (data.invalid) {
        delete data.invalid;
        const updatedYaml = yaml.dump(data, { 
          lineWidth: -1,
          noCompatMode: true,
          quotingType: '"',
          forceQuotes: false
        });
        fs.writeFileSync(filePath, updatedYaml);
        return { updated: true };
      }
      return { updated: false };
    } else {
      console.log(`✗ NOT FOUND: ${domain}`);
      
      // Mark as invalid if not already marked
      if (!data.invalid) {
        data.invalid = true;
        const updatedYaml = yaml.dump(data, { 
          lineWidth: -1,
          noCompatMode: true,
          quotingType: '"',
          forceQuotes: false
        });
        fs.writeFileSync(filePath, updatedYaml);
        return { updated: true };
      }
      return { updated: false };
    }
  } catch (error) {
    console.error(`ERROR processing ${filePath}: ${error.message}`);
    return { updated: false };
  }
}

async function main() {
  try {
    const files = fs.readdirSync(NAMES_DIR)
      .filter(file => file.endsWith('.yml'))
      .map(file => path.join(NAMES_DIR, file));

    console.log(`Found ${files.length} YAML files to process\n`);

    let processedCount = 0;
    let updatedCount = 0;
    let foundCount = 0;
    let notFoundCount = 0;

    for (const file of files) {
      const result = await processYamlFile(file);
      processedCount++;
      
      if (result.updated) {
        updatedCount++;
      }

      // Small delay to be respectful to servers
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    console.log(`\n--- SUMMARY ---`);
    console.log(`Processed: ${processedCount} files`);
    console.log(`Updated: ${updatedCount} files`);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();