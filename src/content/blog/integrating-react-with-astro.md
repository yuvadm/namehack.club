---
title: "Integrating React with Astro"
description: "Learn how to use React components within your Astro website for interactive UI elements."
pubDate: 2025-05-21
image: "https://images.unsplash.com/photo-1633356122102-3fe601e05bd2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80"
author: "React Expert"
tags: ["astro", "react", "integration", "web development"]
---

# Integrating React with Astro

Astro allows you to use React components alongside static content, giving you the best of both worlds: the performance of static HTML with the interactivity of React when needed.

## Setting Up React in Astro

First, you'll need to install the React integration:

```bash
npm install @astrojs/react react react-dom
```

Then, update your `astro.config.mjs` file:

```javascript
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';

export default defineConfig({
  integrations: [react()]
});
```

## Creating React Components

Create your React components as you normally would:

```jsx
// src/components/Counter.jsx
import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
```

## Using React Components in Astro

Import and use your React components in Astro files:

```astro
---
import Counter from '../components/Counter';
---

<div>
  <h1>My Astro Site</h1>
  <Counter client:load />
</div>
```

The `client:load` directive tells Astro to hydrate this component on page load, making it interactive.

## Client Directives

Astro provides several client directives to control when React components are hydrated:

- `client:load`: Hydrate the component on page load
- `client:idle`: Hydrate when the browser is idle
- `client:visible`: Hydrate when the component is visible in the viewport
- `client:media`: Hydrate when a media query is matched
- `client:only`: Skip server-rendering and only render on the client

## Conclusion

By combining Astro's static-first approach with React's interactivity, you can build fast, responsive websites that provide excellent user experiences without sacrificing developer experience.
