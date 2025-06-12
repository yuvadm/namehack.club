---
title: "Using Tailwind CSS in Astro"
description: "Learn how to integrate and use Tailwind CSS to style your Astro website efficiently."
pubDate: 2025-05-22
image: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80"
author: "CSS Enthusiast"
tags: ["astro", "tailwind", "css", "styling"]
---

# Using Tailwind CSS in Astro

Tailwind CSS is a utility-first CSS framework that can be seamlessly integrated with Astro to create beautiful, responsive websites without writing custom CSS.

## Setting Up Tailwind in Astro

To get started with Tailwind CSS in your Astro project, you'll need to install the necessary dependencies:

```bash
npm install -D @tailwindcss/vite tailwindcss
```

Next, create a configuration file for Tailwind:

```bash
npx tailwindcss init
```

Update your `tailwind.config.js` file:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

## Integrating with Astro

Update your `astro.config.mjs` file to use the Tailwind plugin:

```javascript
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  vite: {
    plugins: [tailwindcss()]
  }
});
```

Create or update your global CSS file to include Tailwind's directives:

```css
/* src/styles/global.css */
@import "tailwindcss";
```

Import this CSS file in your layout or components:

```astro
---
import '../styles/global.css';
---
```

## Using Tailwind Classes

Now you can use Tailwind's utility classes directly in your HTML:

```astro
<div class="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl">
  <div class="md:flex">
    <div class="md:shrink-0">
      <img class="h-48 w-full object-cover md:h-full md:w-48" src="/img/example.jpg" alt="Example">
    </div>
    <div class="p-8">
      <div class="uppercase tracking-wide text-sm text-indigo-500 font-semibold">Case study</div>
      <a href="#" class="block mt-1 text-lg leading-tight font-medium text-black hover:underline">Finding customers for your new business</a>
      <p class="mt-2 text-slate-500">Getting a new business off the ground is a lot of hard work. Here are five ideas you can use to find your first customers.</p>
    </div>
  </div>
</div>
```

## Tailwind Typography Plugin

For styling markdown content, the Typography plugin is extremely useful:

```bash
npm install -D @tailwindcss/typography
```

Add it to your Tailwind config:

```javascript
// tailwind.config.js
module.exports = {
  // ...
  plugins: [
    require('@tailwindcss/typography'),
    // ...
  ],
}
```

Then use the `prose` class on your markdown content:

```astro
<article class="prose lg:prose-xl">
  <!-- Your markdown content will be styled nicely -->
  <slot />
</article>
```

## Conclusion

Tailwind CSS provides a powerful and efficient way to style your Astro website. With its utility-first approach, you can rapidly build custom designs without leaving your HTML or writing custom CSS.
