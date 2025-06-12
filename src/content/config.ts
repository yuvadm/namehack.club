import { defineCollection, z } from 'astro:content';

// Define the blog collection schema
const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    image: z.string().optional(),
    author: z.string().default('Anonymous'),
    tags: z.array(z.string()).default([]),
  }),
});

// Export the collections
export const collections = {
  'blog': blogCollection,
};
